from sqlmodel import Field, Relationship,  SQLModel
from datetime import datetime

class AliasBase(SQLModel):
    id: int | None
    created_at: datetime | None
    updated_at: datetime | None


class AliasResponse(AliasBase):
    pass

class Alias(AliasBase, table=True):
    __tablename__: str = "aliases"
    id: int | None = Field(default=None, primary_key=True)
    name: str | None
    emailaddress: str | None
    description: str | None