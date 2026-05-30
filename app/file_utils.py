import datetime
from fastapi import UploadFile, HTTPException
import hashlib
from pathlib import Path
import os
from .dependencies import Database
from .time_utils import now
from datetime import datetime


from .models.files import File

def generate_unique_filename(upload_file: UploadFile) -> str:
    original_name = upload_file.filename or "upload"
    timestamp = datetime.utcnow().isoformat()
    hash_input = f"{original_name}-{timestamp}".encode()
    hashed = hashlib.sha1(hash_input).hexdigest()
    extension = os.path.splitext(original_name)[1]
    return f"{hashed}{extension}"

async def store_file(database: Database, file: UploadFile, path: Path) -> File:
    try:
        filename = generate_unique_filename(file)
        file_path = path / filename

        with open(file_path, "wb") as f:
            f.write(await file.read())

        # TODO: Compress file and create thumbnail

        # Upload File
        file_size  = os.path.getsize(file_path)
        t = now()
        db_file = File(
            file_name = filename,
            content_type=file.content_type,
            path='/' + str(path / filename),
            size=file_size,
            created_at=t,
            updated_at=t,
        )
        database.add(db_file)
        await database.commit() # Retrieves id of the File
        await database.refresh(db_file)

        return db_file

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to upload photo")
