from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlmodel import SQLModel, select, func, and_, text
from pydantic import ValidationError
from sqlalchemy.orm import selectinload
from ..dependencies import Database
from ..models.event import *


router = APIRouter(prefix="/events")

@router.get("", response_model=list[EventResponse])
async def get_all(r: Request, database: Database):
    query = select(Event) \
        .order_by(Event.created_at.desc())

    events = await database.exec(query)
    return [EventResponse.model_validate(event) for event in events.all()]

@router.get("/{id}", response_model=EventResponse)
async def get(id: int, r: Request, db: Database):
    query = (
        select(Event, Result) \
        .where(Event.id == id)
        .join(Result, Event.id == Result.event_id)
    )
    
    rows = await db.exec(query)
    rows = rows.all()
    event = rows[0].Event
    results = [
        ResultResponse.model_validate(row.Result)
        for row in rows
    ]
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventResponse(
        id=event.id,
        created_at=event.created_at,
        updated_at=event.updated_at,
        date=event.date,
        eventtype_id=event.eventtype_id,
        agendaitem_id=event.agendaitem_id,
        distance=event.distance,
        results=results
    )

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