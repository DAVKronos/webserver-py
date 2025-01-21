from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Request, Depends, Query , HTTPException 
from fastapi.responses import JSONResponse
from sqlalchemy import column, func
from sqlmodel import select
from ..dependencies import Database
from ..models.agendaitem import *
from ..models.agendaitemtype import *

router = APIRouter()

@router.get("/agendaitems", response_model = list[AgendaitemResponse])
async def get_all(r: Request, database: Database, year: Annotated[int | None, Query(alias="date[year]")] = None,
              month: Annotated[int | None, Query(alias="date[month]")] = None):
    
    query = select(Agendaitem) \
        .order_by(Agendaitem.created_at.desc())
    if year is not None: query = query.where(func.extract("year", Agendaitem.date) == year)
    if month is not None: query = query.where(func.extract("month", Agendaitem.date) == month)

    agendaitems = await database.exec(query)
    return [AgendaitemResponse.model_validate(agendaitem) for agendaitem in agendaitems.all()]

@router.get("/agendaitems/{id}", response_model=AgendaitemResponse)
async def get(id : int , r: Request, database: Database):
    agendaitem = await database.get(Agendaitem,id) 
    if agendaitem is None : 
        raise HTTPException(status_code=404, detail="Agenda item not found")
    return agendaitem

#/agendaitemtypes
@router.get("/agendaitemtypes/{id}", response_model=AgendaitemTypeResponse)
async def get(id:int, r: Request, database: Database):
    agendaitemtype = await database.get(AgendaitemType, id)
    if agendaitemtype is None: 
        raise HTTPException(status_code=404, detail="Agenda item type not found")
    return agendaitemtype

@router.get("/agendaitems/{id}/events", response_class=JSONResponse)
async def get(r: Request, database: Database):
    pass


@router.get("/agendaitems/{id}/subscriptions", response_class=JSONResponse)
async def get(r: Request, database: Database):
    pass
