
from typing import Annotated
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from ..dependencies import DepDatabase
from ..queries import documents

router = APIRouter(prefix="")



@router.get("/folders", response_class=JSONResponse)
async def get(r: Request, database: DepDatabase):
    res = await documents.get_folders(database)
    return res

@router.get("/folders/{id}", response_class=JSONResponse)
async def get(id: int, r: Request, database: DepDatabase):
    res = await documents.get_folders(database, id)
    return res

@router.get("/kronometers", response_class=JSONResponse)
async def get( r: Request, database: DepDatabase):
    res = await documents.get(database)
    return res

@router.get("/folders/{id}/kronometers", response_class=JSONResponse)
async def get(id: int, r: Request, database: DepDatabase):
    res = await documents.get(database, id)
    return res
