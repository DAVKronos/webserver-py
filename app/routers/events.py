from typing import Annotated
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from ..database.pg import get_database
from ..queries import events
from datetime import datetime
router = APIRouter(prefix="/events")

@router.get("/", response_class=JSONResponse)
async def get(r: Request, database: Annotated[dict, Depends(get_database)]):
    res = await events.get(database)
    return res

@router.get("/{id}", response_class=JSONResponse)
async def get(id: int, r: Request, db: Annotated[dict, Depends(get_database)]):
    res = await events.get(db, id)
    return res
