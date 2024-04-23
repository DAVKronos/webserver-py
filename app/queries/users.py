from sqlalchemy import column, select, func
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

async def get_password(database, username: str):
    q = select(users.c.email, users.c.encrypted_password) \
        .where(func.lower(column("email")) == func.lower(username)) 
    
    r = await database.fetch_one(query=q)
    return r
