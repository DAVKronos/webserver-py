from sqlalchemy import column, select
from ..schemas import photos, photo_albums

async def get(database, album_id: int = None):
    query = photos.select()
    query = query.where(column("photoalbum_id") == album_id)
    
    rows = await database.fetch_all(query=query)
    return [dict(r._mapping) for r in rows]

async def get_albums(database, id: int = None):
    query = photo_albums.select()
    if id is not None:
        query = query.where(column("id") == id)

    rows = await database.fetch_all(query=query)
    return [dict(r._mapping) for r in rows]
