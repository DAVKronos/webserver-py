from sqlalchemy import column, select, func
from ..schemas import agendaitems

async def get(database, id: int = None):
    query = agendaitems.select()
    if id is not None: query = query.where(agendaitems.c.id == id)
    
    rows = await database.fetch_all(query=query)
    return [dict(r._mapping) for r in rows]

async def get_by_date(database, year: int = None, month: int = None):
    
    q = select(agendaitems)
    if year is not None: q = q.where(func.extract("year", agendaitems.c.date) == year)
    if month is not None: q = q.where(func.extract("month", agendaitems.c.date) == month)
    
    rows = await database.fetch_all(q)
    return [dict(r._mapping) for r in rows]
