import re
from datetime import datetime
from sqlalchemy import text

async def migrate_table(old_conn, new_conn, old_table, new_table, col_mapping, fk_mapping={}, migration_criteria=None):
    print(f"Starting {new_table} migration...")
    res = await old_conn.execute(text(f"SELECT * FROM {old_table}"))
    rows = res.mappings().all()
    
    if not rows:
        print(f"No rows found in {old_table}. Skipping.")
        return

    valid_refs = await get_valid_references(new_conn, fk_mapping)
    to_insert = []
    invalid_ref_count = 0

    for row in rows:
        # Filter data if a function is given
        if migration_criteria and not migration_criteria(row):
            continue # Do not migrate this row
        
        # Invert mapping: map[old_column] = new_column
        data = {new_k: row[old_k] for old_k, new_k in col_mapping.items() if old_k in row}

        # TODO: Maybe have a better policy for non-existing references
        for fk_col, ids in valid_refs.items():
            if data.get(fk_col) not in ids:
                invalid_ref_count += 1
                data[fk_col] = None
        
        to_insert.append(data)

    await bulk_insert(new_conn, to_insert, new_table)
    
    await update_sequence(new_conn, new_table)
    print(f"Finished {new_table} migration. Inserted {len(to_insert)} rows with {invalid_ref_count} invalid refs.")

async def migrate_self_referencing_table(old_conn, new_conn, old_table, new_table, col_mapping, self_mapping_col):
    print(f"Starting self-referencing {new_table} migration...")
    res = await old_conn.execute(text(f"SELECT * FROM {old_table} ORDER BY id ASC"))
    rows = res.mappings().all()
    invalid_ref_count = 0
    valid_ids = set()
    to_insert = []

    for row in rows:
        data = {new_k: row[old_k] for old_k, new_k in col_mapping.items() if old_k in row}
        
        # Check if the self_mapping_col exists in the set
        parent_id = data.get(self_mapping_col)
        if parent_id and parent_id not in valid_ids:
            print(f"Parent {parent_id} not found for {data['id']}. Setting to NULL.")
            data[self_mapping_col] = None
            invalid_ref_count += 1
        to_insert.append(data)
        valid_ids.add(data["id"])

    if len(to_insert) != 0:
        await bulk_insert(new_conn, to_insert, new_table)

    await update_sequence(new_conn, "document_folders")
    print(f"Finished {new_table} migration. Inserted {len(to_insert)} rows with {invalid_ref_count} invalid refs.")

async def get_valid_references(conn, fk_mapping):
    valid_refs = {}
    for col, ref_table in fk_mapping.items():
        ref_res = await conn.execute(text(f"SELECT id FROM {ref_table}"))
        valid_refs[col] = {r[0] for r in ref_res.fetchall()} # Save valid id's for each ref
        valid_refs[col].add(None) # count NULL ref as valid ref
    return valid_refs

async def bulk_insert(conn, to_insert, table):
    cols = ", ".join(to_insert[0].keys())
    placeholders = ", ".join([f":{k}" for k in to_insert[0].keys()])
    stmt = text(f"INSERT INTO {table} ({cols}) VALUES ({placeholders})")
    await conn.execute(stmt, to_insert)

async def update_sequence(conn, table):
    try:
        await conn.execute(text(f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), COALESCE((SELECT MAX(id) FROM {table}), 1))"))
    except Exception as e:
        print(f"Warning: Could not update sequence: {e}")

# Do not migrate deleted users
def user_criteria(row):
    regex = r"x\d+.*" # Filter strings like x70 (may have a suffix)
    return not bool(re.fullmatch(regex, row["name"]))

# Create a file for each row and updating the corresponding row's file_id
async def migrate_table_file(old_conn, new_conn, old_table, new_table, field_names, file_id_field):
    print(f"Starting {new_table} file migration...")
    
    res = await old_conn.execute(text(f"SELECT id, {', '.join(field_names.values())} FROM {old_table}"))
    rows = res.mappings().all()
    rows_with_file = [r for r in rows if r[field_names["path"]] is not None]
    
    if not rows_with_file:
        return

    new_file_ids = await upload_files(new_conn, rows_with_file, field_names)
    
    updates = [
        {"table_id": rows_with_file[i]["id"], "file_id": new_file_ids[i]}
        for i in range(len(rows_with_file))
    ]

    update_stmt = text(f"UPDATE {new_table} SET {file_id_field} = :file_id WHERE id = :table_id")
    await new_conn.execute(update_stmt, updates)

    print(f"Finished {new_table} photo migration. Inserted {len(new_file_ids)} files and updated {len(updates)} rows.")

async def migrate_photos(old_conn, new_conn):
    print("Starting photo migration...")
    res = await old_conn.execute(text("SELECT * FROM photos"))
    rows = res.mappings().all()

    field_names = {
        "file_name": "photo_file_name",
        "content_type": "photo_content_type",
        "file_size": "photo_file_size",
        "updated_at": "photo_updated_at"
    }
    new_file_ids = await upload_files(new_conn, rows, field_names)

    valid_refs = await get_valid_references(new_conn, {"photoalbum_id": "photo_albums"})
    invalid_ref_count = 0

    to_insert = []
    for i, row in enumerate(rows):
        data = {
            "id": row["id"],
            "file_id": new_file_ids[i],
            "photoalbum_id": row["photoalbum_id"],
            "exif_date": row["exif_date"],
            "url": row["photo_url_original"],
            "thumbnail_url": row["photo_url_thumb"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"]
        }

        if data["photoalbum_id"] not in valid_refs["photoalbum_id"]:
            data["photoalbum_id"] = None
            invalid_ref_count += 1
        
        to_insert.append(data)
    
    await bulk_insert(new_conn, to_insert, "photos")
    print(f"Finished photo migration. Inserted {len(new_file_ids)} files and {len(to_insert)} photos with {invalid_ref_count} invalid refs.")

async def upload_files(conn, rows, field_names):
    chunk_size = 5000
    all_new_ids = []
    
    # We apparently need to process rows in chunks to avoid a 32767 parameter limit
    for i in range(0, len(rows), chunk_size):
        chunk = rows[i : i + chunk_size]
        params = {}
        value_strings = []
        
        for j, r in enumerate(chunk):
            # Unique keys within this specific chunk
            params.update({
                f"fn_{j}": r[field_names["path"]],
                f"ct_{j}": r[field_names["content_type"]],
                f"fs_{j}": r[field_names["file_size"]],
                f"ua_{j}": r[field_names["updated_at"]]
            })
            value_strings.append(f"(:fn_{j}, :ct_{j}, :fs_{j}, :ua_{j})")

        stmt_text = f"""
            INSERT INTO files (path, content_type, file_size, updated_at) 
            VALUES {', '.join(value_strings)} 
            RETURNING id
        """
        
        result = await conn.execute(text(stmt_text), params)
        chunk_ids = [r[0] for r in result.all()]
        all_new_ids.extend(chunk_ids)
        
    return all_new_ids