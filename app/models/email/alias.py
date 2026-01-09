############### UPDATED #################
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

class MailAliasBase(SQLModel):
    id: int
    name: Optional[str] = None
    email_address: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class MailAlias(MailAliasBase, table=True):
    __tablename__ = "mail_aliases"
    id: Optional[int] = Field(default=None, primary_key=True)

class MailAliasResponse(MailAliasBase):
    pass