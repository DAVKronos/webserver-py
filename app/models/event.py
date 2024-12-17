from sqlmodel import Field, Relationship,  SQLModel
from datetime import datetime, time

class EventBase(SQLModel):
    id: int | None
    created_at: datetime | None
    updated_at: datetime | None
    date: time | None
    eventtype_id: int | None
    agendaitem_id: int | None
    distance: float | None

class EventResponse(EventBase):
    pass

class Event(EventBase, table=True):
    __tablename__: str = "events"
    id: int | None = Field(default=None, primary_key=True)


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
    distance: float | None



class EventCreate(SQLModel):
    event: str
    event_en: str
    news: str
    news_en: str


class EventTypeResponse(EventTypeBase):
    pass

class EventType(EventTypeBase, table=True):
    __tablename__: str = "eventtypes"
    id: int | None = Field(default=None, primary_key=True)





