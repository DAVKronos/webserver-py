from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy import column, select, func
from ..dependencies import Database
from ..models.agendaitem import *
from ..models.agendaitemtype import *

router = APIRouter()

from app import dependencies as deps
from app.models import AgendaitemResponse
# date[year]=&date[month]=
@router.get("/agendaitems", response_model= list[AgendaitemResponse])
async def index(r: Request, database: Database, year: Annotated[int | None, Query(alias="date[year]")] = None,
              month: Annotated[int | None, Query(alias="date[month]")] = None):
    
    query = select(Agendaitem) \
        .order_by(Agendaitem.created_at.desc())
    if year is not None: query = query.where(func.extract("year", Agendaitem.date) == year)
    if month is not None: query = query.where(func.extract("month", Agendaitem.date) == month)

    agendaitems = await database.exec(query)

    # TODO: as a constructor on AgendaitemResponse
    def to_response(row):
        ait = AgendaitemTypeResponse(**row.agendaitemtype.dict()) if row.agendaitemtype is not None else None
        sbs = [SubscriptionResponse(**s.dict()) for s in row.subscriptions]
        return AgendaitemResponse(**row.dict(), agendaitemtype=ait, subscriptions=sbs)
        
    return [to_response(r) for (r,) in agendaitems.all()]



@router.get("/agendaitems/{id}", response_class=JSONResponse)
async def get(r: Request, database: Database):
    pass

#/agendaitemtypes
@router.get("/agendaitemtypes/{id}", response_class=JSONResponse)
async def get(r: Request, database: Database):
    pass

@router.get("/agendaitems/{id}/events", response_class=JSONResponse)
async def get(r: Request, database: Database):
    pass


@router.get("/agendaitems/{id}/subscriptions", response_class=JSONResponse)
async def get(r: Request, database: Database):
    pass
