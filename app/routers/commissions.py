from typing import Annotated
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from ..dependencies import DepDatabase
from ..queries import commissions
from datetime import datetime
router = APIRouter(prefix="/commissions")

@router.get("/", response_class=JSONResponse)
async def get(r: Request, database: DepDatabase):
    res = await commissions.get(database)
    return res

@router.get("/{id}", response_class=JSONResponse)
async def get(id: int, r: Request, db: DepDatabase):
    res = await commissions.get(db, id)
    return res

@router.get("/{id}/commission_memberships", response_class=JSONResponse)
async def get(id: int, r: Request, db: DepDatabase):
    res = await commissions.get_memberships(db, id)
    return res
