from sqlmodel import Field, Relationship,  SQLModel
from datetime import datetime

class AliasMailinglistBase(SQLModel):
    id: int | None
    created_at: datetime | None
    updated_at: datetime | None


class AliasMailinglistResponse(AliasMailinglistBase):
    pass

class AliasMailinglist(AliasMailinglistBase, table=True):
    __tablename__: str = "aliases_mailinglists"
    id: int | None = Field(default=None, primary_key=True)
    alias_id: int | None 
    mailinglist_id: int | None 