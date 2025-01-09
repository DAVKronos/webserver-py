from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Request, Depends, Query, HTTPException
from sqlmodel import SQLModel, select, func
from sqlalchemy import extract
from ..dependencies import Database
from ..models.result import *

router = APIRouter(prefix="/results")

@router.get("")
async def get_all(
    r: Request, 
    db: Database,
    year: Annotated[int | None, Query(alias="date[year]")] = None,
    month: Annotated[int | None, Query(alias="date[month]")] = None
):
    
    query = select(Result) \
        .order_by(Result.created_at.desc())
    
    if year:
        query = query.where(extract('year', Result.updated_at) == year)
    if month:
        query = query.where(extract('month', Result.updated_at) == month)
    results = await db.exec(query)
    return [ResultResponse.model_validate(result) for result in results.all()]



@router.get("/{id}", response_model=ResultResponse)
async def get(id: int, r: Request, db: Database):
    result = await db.get(Result, id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return ResultResponse.model_validate(result)