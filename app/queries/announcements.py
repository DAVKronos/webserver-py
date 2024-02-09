from sqlalchemy import column
from ..schemas import announcements

async def get(database, active=None):
    query = announcements.select()
    if active is not None:
        query = query.where(column("starts_at") < active) \
                     .where(column("ends_at") > active)
    rows = await database.fetch_all(query=query)
    return [dict(r._mapping) for r in rows]
