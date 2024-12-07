from typing import Annotated
from fastapi import APIRouter, Request, Depends
from ..dependencies import Database
from ..models.result import *

router = APIRouter(prefix="/results")

@router.get("", response_model=list[ResultResponse])
async def get_all(r: Request, database: Database):
    query = select(Result) \
        .order_by(Result.created_at.desc())

    results = await database.exec(query)
    return results.all()
