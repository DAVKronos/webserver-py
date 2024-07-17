from sqlalchemy import column, select
from ..schemas import results

async def get(database, id: int = None):
    query = results.select()
    if id is not None:
        query = query.where(column("id") == id)

    rows = await database.fetch_all(query=query)
    return [dict(r._mapping) for r in rows]

