from sqlalchemy import column, select
from ..schemas import commissions, commission_memberships, users

async def get(database, id: int = None):
    query = commissions.select()
    if id is not None:
        query = query.where(column("id") == id)

    rows = await database.fetch_all(query=query)
    return [dict(r._mapping) for r in rows]

async def get_memberships(database, id: int):
    query = select(commission_memberships.c.id,
                   commission_memberships.c.function,
                   commission_memberships.c.installed,
                   commission_memberships.c.commission_id,
                   commission_memberships.c.user_id,
                   commission_memberships.c.created_at,
                   commission_memberships.c.updated_at,
                   users.c.name) \
        .join_from(users, commission_memberships) \
        .join_from(commission_memberships, commissions) \
        .where(commissions.c.id == id)
    
    rows = await database.fetch_all(query=query)
    def nest(r):
        d = dict(r)
        d["user"]={"name":d["name"]}
        return d
    
    return [nest(r._mapping) for r in rows]
