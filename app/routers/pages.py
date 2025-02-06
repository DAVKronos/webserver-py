from sqlmodel import select
from typing import Annotated
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlmodel import select
from ..dependencies import Database
from ..models.page import *

router = APIRouter(prefix="/pages")

@router.get("", response_model=list[PageResponse])
async def get_all(r: Request, database: Database):
    query = select(Page) \
        .order_by(Page.pagetag.desc())

    pages = await database.exec(query)
    return pages.all()

@router.get("/{id}", response_model=PageResponse)
async def get(id: int, r: Request, database: Database):
    page = database.get(page, id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page