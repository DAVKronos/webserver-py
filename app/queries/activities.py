from sqlalchemy import column, select, func
from ..schemas import agendaitems, agendaitem_types, subscriptions, events, results
from itertools import groupby
from functools import reduce


async def get(database, id: int = None):
    query = select(agendaitems, agendaitem_types.c.name.label("agendaitemtype")) \
        .join(agenda_item_types, agendaitems.c.agendaitemtype_id == agendaitem_types.c.id, isouter=True)
    if id is not None: query = query.where(agendaitems.c.id == id)
    
    rows = await database.fetch_all(query=query)
    return rows

async def get_by_date(database, year: int = None, month: int = None):
    q = select(agendaitems, agendaitem_types.c.name, subscriptions.c.id) \
        .join(agendaitem_types, agendaitems.c.agendaitemtype_id == agendaitem_types.c.id, isouter=True) \
        .join(subscriptions) \
        .order_by(agendaitems.c.id) \
        .apply_labels()
    
    if year is not None: q = q.where(func.extract("year", agendaitems.c.date) == year)
    if month is not None: q = q.where(func.extract("month", agendaitems.c.date) == month)
    
    rows = await database.fetch_all(q)
    
    agendaitems_keys = {c: c.split("agendaitems_")[1] for c in q.c.keys() if c.startswith("agendaitems_")}
    subscriptions_keys = {c: c.split("subscriptions_")[1] for c in q.c.keys() if c.startswith("subscriptions_")}
    
    def into_object(a,b):
        b = b._mapping
        if a is None:
            print(list(b.keys()))
            a = {v: b[k] for k,v in agendaitems_keys.items()}
            a.update({"subscriptions": [], "agendaitemtype": {"name": b['agendaitemtypes_name']}})
        r = {v: b[k] for k,v in subscriptions_keys.items()}
        if r["id"] is not None: a["subscriptions"].append(r)
        return a
    
    sorted(rows, key=lambda x: x.agendaitems_id)
    
    grouped = groupby(rows, lambda x: x.agendaitems_id)
    return [reduce(into_object, g, None) for _,g in grouped]

