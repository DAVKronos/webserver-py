from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime, time

class EventBase(SQLModel):
    id: int | None
    created_at: datetime | None
    updated_at: datetime | None
    date: time | None
    eventtype_id: int | None
    agendaitem_id: int | None
    distance: float | None


class EventTypeBase(SQLModel):
    id: int | None
    created_at: datetime | None
    updated_at: datetime | None
    name: str | None
    shortname: str | None
    formula: str | None
    female_formula: str | None
    measuringunit: str | None
    calculated_unit: str | None
    show_wind: bool | None
    important: bool | None

class EventCreate(SQLModel):
    event: str
    event_en: str
    news: str
    news_en: str

class EventTypeResponse(EventTypeBase):
    pass

class EventResponse(EventBase):
    eventtype: EventTypeResponse | None = None
    results: list["ResultResponse"] = []

class EventType(EventTypeBase, table=True):
    __tablename__: str = "eventtypes"
    id: int | None = Field(default=None, primary_key=True)
    events: list["Event"] = Relationship(back_populates="eventtype")


class Event(EventBase, table=True):
    __tablename__: str = "events"
    id: int | None = Field(default=None, primary_key=True)
    eventtype_id: int | None = Field(default=None, foreign_key="eventtypes.id")
    eventtype: EventType = Relationship(back_populates="events", sa_relationship_kwargs={"lazy": "selectin"})
    results: list["Result"] = Relationship(back_populates="event", sa_relationship_kwargs={"lazy": "selectin"})

from .result import ResultResponse

