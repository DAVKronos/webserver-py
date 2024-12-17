from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Request, Depends
from sqlmodel import select
from ..dependencies import Database
from ..models.event import *
router = APIRouter(prefix="/events")

@router.get("", response_model=list[EventResponse])
async def get_all(r: Request, database: Database):
    query = select(Event) \
        .order_by(Event.name.desc())

    events = await database.exec(query)
    return events.all()

@router.get("/{id}", response_model=EventResponse)
async def get(id: int, r: Request, db: Database):
    event = await db.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventResponse.model_validate(event)