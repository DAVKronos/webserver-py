from typing import Annotated
from fastapi import APIRouter, Request, Depends, Query
from fastapi.responses import JSONResponse
from ..database.pg import get_database
from ..queries import activities
from datetime import datetime
router = APIRouter(prefix="")

# date[year]=&date[month]=
@router.get("/agendaitems", response_class=JSONResponse)
async def get(database: Annotated[dict, Depends(get_database)],
              year: Annotated[int | None, Query(alias="date[year]")] = None,
              month: Annotated[int | None, Query(alias="date[month]")] = None):
    res = await activities.get_by_date(database, year, month)
    return res


@router.get("/agendaitems/{id}", response_class=JSONResponse)
async def get(r: Request, database: Annotated[dict, Depends(get_database)]):
    pass
    #res = await announcements.get(database, active=datetime.now())


#/agendaitemtypes
@router.get("/agendaitemtypes/{id}", response_class=JSONResponse)
async def get(r: Request, database: Annotated[dict, Depends(get_database)]):
    pass

@router.get("/agendaitems/{id}/events", response_class=JSONResponse)
async def get(r: Request, database: Annotated[dict, Depends(get_database)]):
    pass


@router.get("/agendaitems/{id}/subscriptions", response_class=JSONResponse)
async def get(r: Request, database: Annotated[dict, Depends(get_database)]):
    pass
