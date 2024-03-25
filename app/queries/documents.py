from sqlalchemy import column, select
from ..schemas import folders, kronometers

async def get(database, folder_id: int = None):
    query = kronometers.select()
    query = query.where(column("folder_id") == folder_id)
    
    rows = await database.fetch_all(query=query)
    return [dict(r._mapping) for r in rows]

async def get_folders(database, id: int = None):
    query = folders.select()
    if id is not None:
        query = query.where(column("id") == id)

    rows = await database.fetch_all(query=query)
    return [dict(r._mapping) for r in rows]

