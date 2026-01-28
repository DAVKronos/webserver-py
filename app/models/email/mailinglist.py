############### UPDATED #################
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from ..user import UserResponse, User

############ MAILING LIST
class MailingListBase(SQLModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    local_part: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class MailingList(MailingListBase, table=True):
    __tablename__ = "mailing_lists"
    id: Optional[int] = Field(default=None, primary_key=True)
    members: "MailingListMember" = Relationship(back_populates="mailing_list",sa_relationship_kwargs={"lazy": "selectin"})

class MailingListResponse(MailingListBase):
    pass

################ MAILING LIST MEMBERSHIPS

class MailingListMemberBase(SQLModel):
    id: int
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    mailing_list_id: Optional[int] = Field(default=None, foreign_key="mailing_lists.id")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class MailingListMember(MailingListMemberBase, table=True):
    __tablename__ = "mailing_list_members"
    id: Optional[int] = Field(default=None, primary_key=True)
    user: "User" = Relationship(back_populates="mailing_list_memberships",sa_relationship_kwargs={"lazy": "selectin"})
    mailing_list: "MailingList" = Relationship(back_populates="members", sa_relationship_kwargs={"lazy": "selectin"})

class MailingListMemberResponse(MailingListMemberBase):
    user: "UserResponse"
    mailing_list: "MailingList"
