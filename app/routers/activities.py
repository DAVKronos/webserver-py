from typing import Annotated
from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import JSONResponse
from ..dependencies import DepDatabase
from ..queries import activities
from datetime import datetime
router = APIRouter()

# date[year]=&date[month]=
@router.get("/agendaitems", response_class=JSONResponse)
async def get(database: DepDatabase,
              year: Annotated[int | None, Query(alias="date[year]")] = None,
              month: Annotated[int | None, Query(alias="date[month]")] = None):
    res = await activities.get_by_date(database, year, month)
    return res


@router.get("/agendaitems/{id}", response_class=JSONResponse)
async def get(r: Request, database: DepDatabase):
    pass
    #res = await announcements.get(database, active=datetime.now())


#/agendaitemtypes
@router.get("/agendaitemtypes/{id}", response_class=JSONResponse)
async def get(r: Request, database: DepDatabase):
    pass

@router.get("/agendaitems/{id}/events", response_class=JSONResponse)
async def get(r: Request, database: DepDatabase):
    pass


@router.get("/agendaitems/{id}/subscriptions", response_class=JSONResponse)
async def get(r: Request, database: DepDatabase):
    pass
