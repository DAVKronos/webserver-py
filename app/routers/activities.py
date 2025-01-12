from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Request, Depends, Query, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import select
from sqlalchemy import column, func
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
    return [x for x,_ in agendaitems.all()]

@router.get("/agendaitems/{id}", response_class=JSONResponse)
async def get(r: Request, database: Database):
    pass

#/agendaitemtypes
@router.get("/agendaitemtypes/{id}", response_model=AgendaitemTypeResponse)
async def get(r: Request, id: int, database: Database):
    agendaitemType = await database.get(AgendaitemType, id)
    if not agendaitemType:
        raise HTTPException(status_code=404, detail="Result not found")
    return AgendaitemTypeResponse.model_validate(agendaitemType)

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
        raise HTTPException(status_code=404, detail="Has no events")
    
    event_results = {}
    for row in rows:
        event_id = row.Event.id
        if event_id not in event_results:
            event_results[event_id] = {
                'event': row.Event,
                'results': []
            }
        event_results[event_id]['results'].append(ResultResponse.model_validate(row.Result))
    
    event_responses = [
        EventResponse(
            id=event_data['event'].id,
            created_at=event_data['event'].created_at,
            updated_at=event_data['event'].updated_at,
            date=event_data['event'].date,
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
