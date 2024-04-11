
from typing import Annotated
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from ..dependencies import DepDatabase
from ..queries import pages

router = APIRouter(prefix="/pages")

@router.get("/", response_class=JSONResponse)
async def get(r: Request, database: DepDatabase):
    res = await pages.get(database)
    return res

@router.get("/{id}", response_class=JSONResponse)
async def get(id: int, r: Request, database: DepDatabase):
    res = await pages.get(database, id)
    return res
