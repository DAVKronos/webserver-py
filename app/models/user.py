from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from .base import TimestampModel
from datetime import datetime, date

# This only runs during type checking, not at runtime
if TYPE_CHECKING:
    from .agendaitem import AgendaItem
    from .news_item import NewsItem
    from .committees import CommitteeMember

class UserBase(TimestampModel):
    name: str
    initials: Optional[str] = None
    email: str = Field(unique=True, index=True)
    birthdate: Optional[date] = None
    address: Optional[str] = None
    postalcode: Optional[str] = None
    city: Optional[str] = None
    sex: Optional[str] = None
    phonenumber: Optional[str] = None
    institution: Optional[str] = None
    joined_in: Optional[int] = None
    avatar_file_id: Optional[int] = None
    user_type_id: Optional[int] = Field(default=None, foreign_key="user_types.id")


class User(UserBase, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    password: str
    bank_account_number: Optional[str] = None
    unioncard_number: Optional[str] = None
    allow_password_change: bool = True
    tokens: Optional[str] = None
    confirmed_at: Optional[datetime] = None

    # Relationships
    created_agenda_items: List["AgendaItem"] = Relationship(back_populates="creator")
    created_news_items: List["NewsItem"] = Relationship(
        back_populates="creator", 
        sa_relationship_kwargs={"foreign_keys": "[NewsItem.creator_id]"}
    )
    approved_news_items: List["NewsItem"] = Relationship(
        back_populates="approver", 
        sa_relationship_kwargs={"foreign_keys": "[NewsItem.approved_by]"}
    )
    committee_memberships: List["CommitteeMember"] = Relationship(
        back_populates="user"
    )
    user_type: Optional["UserType"] = Relationship(
        back_populates="users",
        sa_relationship_kwargs={"foreign_keys": "[User.user_type_id]"}
    )


class UserResponse(UserBase):
    id: int


class UserCreate(SQLModel):
    name: str
    email: str
    password: str
    birthdate: date
    address: str
    postalcode: str
    city: str
    sex: str
    phonenumber: str
    user_type_id: str
    bank_account_number: str
    unioncard_number: str
    institution: str
    joined_in: int

class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    birthdate: Optional[date] = None
    address: Optional[str] = None
    postalcode: Optional[str] = None
    city: Optional[str] = None
    sex: Optional[str] = None
    phonenumber: Optional[str] = None
    bank_account_number: Optional[str] = None
    unioncard_number: Optional[str] = None
    institution: Optional[str] = None
    user_type_id: Optional[int] = None




class UserTypeBase(TimestampModel):
    name_nl: str
    name_en: str
    is_donor: bool = False
    is_competition: bool = False


class UserType(UserTypeBase, table=True):
    __tablename__ = "user_types"

    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationship
    users: List["User"] = Relationship(back_populates="user_type")


class UserTypeResponse(UserTypeBase):
    id: int