from sqlalchemy import column, select
from ..schemas import users, user_types

async def get(database, id: int = None):
    query = users.select()
    if id is not None:
        query = query.where(users.c.id == id)
    
    rows = await database.fetch_all(query=query)
    return [dict(r._mapping) for r in rows]

async def get_usertypes(database, id: int = None):
    query = user_types.select()
    if id is not None:
        query = query.where(column("id") == id)

    rows = await database.fetch_all(query=query)
    return [dict(r._mapping) for r in rows]

