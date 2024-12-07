from sqlmodel import Field, Relationship,  SQLModel
from datetime import datetime

class ResultBase(SQLModel):
    id: int | None
    created_at: datetime | None
    updated_at: datetime | None
    result: str | None
    username: str | None
    calculated: float | None
    wind: float | None
    place: int | None
    event_id: int | None
    user_id: int | None

class ResultResponse(ResultBase):
    pass

class Result(ResultBase, table=True):
    __tablename__: str = "results"
    id: int | None = Field(default=None, primary_key=True)

