from sqlmodel import Field, Relationship,  SQLModel
from datetime import datetime

class MailinglistBase(SQLModel):
    id: int | None
    created_at: datetime | None
    updated_at: datetime | None


class MailinglistResponse(MailinglistBase):
    pass

class Mailinglist(MailinglistBase, table=True):
    __tablename__: str = "mailinglists"
    id: int | None = Field(default=None, primary_key=True)
    commission_id: int | None 
    name: str | None
    description: str | None
    local_part: str | None