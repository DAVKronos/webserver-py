from sqlmodel import Field, Relationship,  SQLModel
from datetime import datetime
from ..commission import CommissionResponse, Commission
from .alias import AliasResponse
from ..user import UserResponse
from typing import List

class MailinglistBase(SQLModel):
    id: int | None
    created_at: datetime | None
    updated_at: datetime | None
    name: str | None
    description: str | None
    local_part: str | None
    commission_id: int| None

class MailinglistResponse(MailinglistBase):
    aliases: List[AliasResponse] = []
    users: List[UserResponse] = []

class Mailinglist(MailinglistBase, table=True):
    __tablename__: str = "mailinglists"
    id: int | None = Field(default=None, primary_key=True)
    commission_id: int | None 
    name: str | None
    description: str | None
    local_part: str | None
