from typing import Annotated
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from ..database.pg import get_database
from ..queries import commissions
from datetime import datetime
router = APIRouter(prefix="/commissions")

@router.get("/", response_class=JSONResponse)
async def get(r: Request, database: Annotated[dict, Depends(get_database)]):
    res = await commissions.get(database)
    return res

@router.get("/{id}", response_class=JSONResponse)
async def get(id: int, r: Request, db: Annotated[dict, Depends(get_database)]):
    res = await commissions.get(db, id)
    return res

@router.get("/{id}/commission_memberships", response_class=JSONResponse)
async def get(id: int, r: Request, db: Annotated[dict, Depends(get_database)]):
    res = await commissions.get_memberships(db, id)
    return res
