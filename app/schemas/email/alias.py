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

class MailAliasResponse(MailAliasBase):
    pass