from typing import Annotated
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from ..dependencies import DepDatabase
from ..queries import articles

router = APIRouter(prefix="/newsitems")

@router.get("/", response_class=JSONResponse)
async def get(r: Request, database: DepDatabase):
    res = await articles.get_published(database)
    return res
@router.get("/{id}", response_class=JSONResponse)
async def get(id: int, r: Request, database: DepDatabase):
    res = await articles.get_published(database, id)
    if len(res) > 0:
        return res[0]
    

@router.get("/{id}/comments", response_class=JSONResponse)
async def get(id: int, r: Request, database: DepDatabase):
    res = await articles.get_comments(database, id)
    return res
