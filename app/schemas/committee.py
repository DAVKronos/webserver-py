############### UPDATED #################
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

# Resolve circular imports
if TYPE_CHECKING:
    from .user import User

############ COMMITTEES
class CommitteeBase(SQLModel):
    id: int
    name_nl: Optional[str] = None
    name_en: Optional[str] = None
    description_nl: Optional[str] = None
    description_en: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CommitteeResponse(CommitteeBase):
    pass

class CommitteeCreate(SQLModel):
    name_nl: str
    name_en: str
    description_nl: str
    description_en: str

############## COMMITTEE MEMBERS

class CommitteeMemberBase(SQLModel):
    id: int
    function: Optional[str] = None
    user_id: Optional[int] = None
    committee_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CommitteeMemberResponse(CommitteeMemberBase):
    pass

class CommitteeMemberCreate(SQLModel):
    id: int
    function: str
