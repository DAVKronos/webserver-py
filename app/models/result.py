from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

class ResultBase(SQLModel):
    id: int | None
    created_at: datetime | None
    updated_at: datetime
    result: str | None
    username: str | None
    calculated: float | None
    wind: float | None
    place: int | None
    user_id: int | None
    event_id: int | None

class Result(ResultBase, table=True):
    __tablename__ = "results"
    id: int | None = Field(default=None, primary_key=True)


class ResultResponse(ResultBase):
    pass