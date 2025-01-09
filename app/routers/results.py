from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Request, Depends, Query, HTTPException
from sqlmodel import SQLModel, select
from ..dependencies import Database
from ..models.result import *

router = APIRouter(prefix="/results")

@router.get("")
async def get_all(r: Request, db: Database):
    query = select(Result) \
        .order_by(Result.created_at.desc())

    results = await db.exec(query)
    return [ResultResponse.model_validate(result) for result in results.all()]



@router.get("/{id}", response_model=ResultResponse)
async def get(id: int, r: Request, db: Database):
    result = await db.get(Result, id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return ResultResponse.model_validate(result)