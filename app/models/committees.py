from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from .base import TimestampModel

from .user import UserBasicResponse
if TYPE_CHECKING:
    from .user import User


# ============================================================
# Committee
# ============================================================

class CommitteeBase(TimestampModel):
    name_nl: str
    name_en: str
    description_nl: str
    description_en: str
    email: Optional[str] = None


class Committee(CommitteeBase, table=True):
    __tablename__ = "committees"

    id: Optional[int] = Field(default=None, primary_key=True)
    role: Optional[str] = None


    memberships: List["CommitteeMember"] = Relationship(back_populates="committee", sa_relationship_kwargs={'lazy': 'selectin'})

class CommitteePublicResponse(CommitteeBase):
    id: int

class CommitteeExtendedResponse(CommitteePublicResponse):
    memberships: List["CommitteeMemberResponse"]


class CommitteeCreate(SQLModel):
    name_nl: str
    name_en: str
    description_nl: str
    description_en: str
    email: Optional[str] = None
    role: Optional[str] = None


class CommitteeUpdate(SQLModel):
    name_nl: Optional[str] = None
    name_en: Optional[str] = None
    description_nl: Optional[str] = None
    description_en: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None


# ============================================================
# Committee Member
# ============================================================

class CommitteeMemberBase(TimestampModel):
    function: Optional[str] = "Member"
    user_id: int = Field(foreign_key="users.id")
    committee_id: int = Field(foreign_key="committees.id")


class CommitteeMember(CommitteeMemberBase, table=True):
    __tablename__ = "committee_members"

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="users.id")
    committee_id: int = Field(foreign_key="committees.id")
    
    user: "User" = Relationship(back_populates="committee_memberships", sa_relationship_kwargs={'lazy': 'selectin'})
    committee: "Committee" = Relationship(back_populates="memberships", sa_relationship_kwargs={'lazy': 'selectin'})


class CommitteeMemberResponse(CommitteeMemberBase):
    id: int
    user: Optional[UserBasicResponse] = None
    committee: Optional[CommitteePublicResponse] = None


class CommitteeMemberCreate(SQLModel):
    user_id: int
    function: Optional[str] = "Member"