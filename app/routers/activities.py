from typing import Annotated
from datetime import datetime, date
from fastapi import APIRouter, Request, Depends, Query, HTTPException , HTTPException 
from fastapi.responses import JSONResponse
from sqlalchemy import column, func
from sqlmodel import select
from ..dependencies import Database
from ..models.agendaitem import *
from ..models.agendaitemtype import AgendaitemTypeResponse
from ..models.result import ResultResponse, Result
from ..models.event import EventResponse, Event

router = APIRouter()

@router.get("/agendaitems", response_model = list[AgendaitemResponse])
async def get(
    r: Request, 
    database: Database, 
    year: Annotated[int, Query(alias="date[year]")] = datetime.now().year,
    month: Annotated[int, Query(alias="date[month]")] = datetime.now().month
):
    query = select(Agendaitem) \
        .order_by(Agendaitem.created_at.desc()) \
        .where(func.extract("year", Agendaitem.date) == year) \
        .where(func.extract("month", Agendaitem.date) == month)

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

@router.get("/agendaitemtypes", response_model=list[AgendaitemTypeResponse])
async def get(r: Request, database: Database):
    query = select(AgendaitemType)
    agendaitemTypes = await database.exec(query) 
    if agendaitemTypes is None : 
        raise HTTPException(status_code=404, detail="Agenda item type not found")
    return agendaitemTypes.all()

@router.get("/agendaitems/{id}/events", response_model=list[EventResponse])
async def get(id: int, r: Request, db: Database):
    query = (
        select(Event) \
        .where(Event.agendaitem_id == id)
    )
    rows = await db.exec(query)
    events = rows.all()

    return events


@router.get("/agendaitems/{id}/subscriptions", response_class=JSONResponse)
async def get(r: Request, database: Database):
    pass
