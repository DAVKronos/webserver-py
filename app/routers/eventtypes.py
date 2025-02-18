from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlmodel import SQLModel, select, func, and_, text
from pydantic import ValidationError
from ..dependencies import Database
from ..models.event import *


router = APIRouter(prefix="/eventtypes")

@router.get("", response_model=list[EventTypeResponse])
async def get_all(r: Request, database: Database):
    query = select(EventType) \
        .order_by(EventType.created_at.desc())

    event_types = await database.exec(query)
    return event_types.all()

@router.get("/{id}", response_model=EventTypeResponse)
async def get(id: int, r: Request, db: Database):
    event_types = await db.get(EventType, id)
    if not event_types:
        raise HTTPException(status_code=404, detail="Event Type not found")
    return event_types

@router.post("/", response_model=EventCreate)
async def create_event(data: EventCreate, database: Database):
    t = datetime.utcnow()
    try:
        event = Event.model_validate(data, update={'created_at': t, 'updated_at': t})
    except ValidationError as e:
        print(e)
        raise HTTPException(status_code=500, detail="Input data not valid")
    
    database.add(event)
    await database.commit()
    await database.refresh(event)
     
    return EventBase.model_validate(event, update={"user":None})