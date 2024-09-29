from sqlalchemy import column, select, func

from app.models import Agendaitem, AgendaitemResponse, AgendaitemType, AgendaitemTypeResponse, Subscription, SubscriptionResponse

async def get(database, id: int):
    pass
    
async def where(database, year: int = None, month: int = None):
    query = select(Agendaitem) \
        .order_by(Agendaitem.id)
    
    if year is not None: query = query.where(func.extract("year", Agendaitem.date) == year)
    if month is not None: query = query.where(func.extract("month", Agendaitem.date) == month)

    result = (await database.exec(query)).all()

    def to_response(row):
        ait = AgendaitemTypeResponse(**row.agendaitemtype.dict()) if row.agendaitemtype is not None else None
        sbs = [SubscriptionResponse(**s.dict()) for s in row.subscriptions]
        return AgendaitemResponse(**row.dict(), agendaitemtype=ait, subscriptions=sbs)
        
    return [to_response(r) for (r,) in result]

