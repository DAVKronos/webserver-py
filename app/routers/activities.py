from typing import Annotated
from datetime import datetime, date
from fastapi import APIRouter, Request, Depends, Query, HTTPException , HTTPException 
from fastapi.responses import JSONResponse
from sqlalchemy import column, select, func
from ..dependencies import Database
from ..models.agendaitem import *
from ..models.agendaitemtype import AgendaitemTypeResponse
from ..models.result import ResultResponse, Result
from ..models.event import EventResponse, Event

router = APIRouter()

@router.get("/agendaitems", response_model = list[AgendaitemResponse])
async def get_all(r: Request, database: Database, year: Annotated[int | None, Query(alias="date[year]")] = None,
              month: Annotated[int | None, Query(alias="date[month]")] = None):
    
    query = select(Agendaitem) \
        .order_by(Agendaitem.created_at.desc())
    if year is not None: query = query.where(func.extract("year", Agendaitem.date) == year)
    if month is not None: query = query.where(func.extract("month", Agendaitem.date) == month)

    agendaitems = await database.exec(query)
    return agendaitems.all()

@router.get("/agendaitems/{id}", response_model=AgendaitemResponse)
async def get(id : int , r: Request, database: Database):
    agendaitem = await database.get(Agendaitem, id) 
    if agendaitem is None : 
        raise HTTPException(status_code=404, detail="Agenda item not found")
    return agendaitem

#/agendaitemtypes
@router.get("/agendaitemtypes/{id}", response_model=AgendaitemTypeResponse)
async def get(id : int , r: Request, database: Database):
    agendaitemType = await database.get(AgendaitemType, id) 
    if agendaitemType is None : 
        raise HTTPException(status_code=404, detail="Agenda item type not found")
    return agendaitemType

@router.get("/agendaitems/{id}/events", response_model=list[EventResponse])
async def get(id: int, r: Request, db: Database):
    query = (
        select(Event, Result) \
        .where(Event.agendaitem_id == id)
        .join(Result, Event.id == Result.event_id)
    )
    
    rows = await db.exec(query)
    rows = rows.all()
    if not rows:
        return []
    
    event_results = {}
    for row in rows:
        event_id = row.Event.id
        if event_id not in event_results:
            event_results[event_id] = {
                'event': row.Event,
                'results': []
            }
        event_results[event_id]['results'].append(row.Result)
    
    event_responses = [
        EventResponse(
            id=event_data['event'].id,
            created_at=event_data['event'].created_at,
            updated_at=event_data['event'].updated_at,
            date=datetime.combine(date.today(), event_data['event'].date),
            eventtype_id=event_data['event'].eventtype_id,
            agendaitem_id=event_data['event'].agendaitem_id,
            distance=event_data['event'].distance,
            results=event_data['results']
        )
        for event_data in event_results.values()
    ]
    
    return event_responses


@router.get("/agendaitems/{id}/subscriptions", response_class=JSONResponse)
async def get(r: Request, database: Database):
    pass
