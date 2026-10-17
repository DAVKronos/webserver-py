from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from .base import TimestampModel

# Put all model imports outside the if statement
from .user import UserBasicResponse

if TYPE_CHECKING:
    # Put all scheme (table) import in the if statement
    from .user import User


class MailingListBase(TimestampModel):
    name: str
    description: Optional[str] = None
    local_part: Optional[str] = None


class MailingList(MailingListBase, table=True):
    __tablename__ = "mailing_lists"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationships
    members: List["User"] = Relationship(
        back_populates="mailing_lists",
        sa_relationship_kwargs={
            "secondary": "mailing_list_members",
            "lazy": "selectin"
        }
    )


class MailingListResponse(MailingListBase):
    id: int
    members: List["UserBasicResponse"] = []


class MailingListUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    local_part: Optional[str] = None


class MailingListCreate(SQLModel):
    name: str
    description: Optional[str] = None
    local_part: Optional[str] = None

 
###############################################################

class MailingListMemberBase(TimestampModel):
    user_id: int = Field(foreign_key="users.id")
    mailing_list_id: int = Field(foreign_key="mailing_lists.id")


class MailingListMember(MailingListMemberBase, table=True):
    __tablename__ = "mailing_list_members"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationships
    user: "User" = Relationship(sa_relationship_kwargs={'lazy': 'selectin'})
    mailing_list: "MailingList" = Relationship()


class MailingListMemberResponse(MailingListMemberBase):
    id: int
    user: UserBasicResponse


class MailingListMemberCreate(SQLModel):
    user_id: int