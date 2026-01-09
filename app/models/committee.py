############### UPDATED #################
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

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

class Committee(CommitteeBase, table=True):
    __tablename__ = "committees"
    id: Optional[int] = Field(default=None, primary_key=True)
    members: list["CommitteeMember"] = Relationship(back_populates="committee")

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
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    committee_id: Optional[int] = Field(default=None, foreign_key="committees.id")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CommitteeMember(CommitteeMemberBase, table=True):
    __tablename__ = "committee_members"
    id: Optional[int] = Field(default=None, primary_key=True)
    user: "User" = Relationship(back_populates="committee_memberships", sa_relationship_kwargs={"lazy": "selectin"})
    committee: "Committee" = Relationship(back_populates="members", sa_relationship_kwargs={"lazy": "selectin"})

class CommitteeMemberResponse(CommitteeMemberBase):
    pass

class CommitteeMemberCreate(SQLModel):
    id: int
    function: str