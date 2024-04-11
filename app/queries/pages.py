from sqlalchemy import column, select
from ..schemas import pages

async def get(database, page_id: int = None):
    q = pages.select()
    if page_id is not None: q = q.where(pages.c.id == page_id)
    rows = await database.fetch_all(q)
    return rows

