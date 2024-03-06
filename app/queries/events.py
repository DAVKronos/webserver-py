from sqlalchemy import column, select
from ..schemas import events

async def get(database, id: int = None):
    query = events.select()
    if id is not None:
        query = query.where(column("id") == id)

    rows = await database.fetch_all(query=query)
    return [dict(r._mapping) for r in rows]

