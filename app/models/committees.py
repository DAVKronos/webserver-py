from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from .base import TimestampModel

from .user import UserResponse

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
    role: Optional[str] = None


class Committee(CommitteeBase, table=True):
    __tablename__ = "committees"

    id: Optional[int] = Field(default=None, primary_key=True)

    memberships: List["CommitteeMember"] = Relationship(back_populates="committee")


class CommitteeResponse(CommitteeBase):
    id: int
    memberships: Optional[List["CommitteeMemberResponse"]] = None


class CompactCommitteeResponse(SQLModel):
    id: int
    name_nl: str
    name_en: str


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
    function: Optional[str] = None
    user_id: int = Field(foreign_key="users.id")
    committee_id: int = Field(foreign_key="committees.id")


class CommitteeMember(CommitteeMemberBase, table=True):
    __tablename__ = "committee_members"

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="users.id")
    committee_id: int = Field(foreign_key="committees.id")
    
    user: "User" = Relationship(back_populates="committee_memberships")
    committee: "Committee" = Relationship(back_populates="memberships")


class CommitteeMemberResponse(CommitteeMemberBase):
    id: int
    user: Optional[UserResponse] = None
    committee: Optional[CompactCommitteeResponse] = None


class CommitteeMemberCreate(SQLModel):
    user_id: int
    function: Optional[str] = None