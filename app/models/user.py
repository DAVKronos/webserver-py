############### UPDATED #################
from typing import Optional, TYPE_CHECKING
from datetime import datetime, date
from sqlmodel import Field, SQLModel, Relationship

# Resolve circular imports
if TYPE_CHECKING:
    from .email.mailinglist import MailingListMember
    from .committee import CommitteeMember
    from .file import File
    from .news_item import NewsItem, NewsComment, Subscription


################ USERS
class UserBase(SQLModel):
    id: int
    name: Optional[str] = None
    initials: Optional[str] = None
    email: Optional[str] = None
    birthdate: Optional[date] = None
    address: Optional[str] = None
    postalcode: Optional[str] = None
    city: Optional[str] = None
    sex: Optional[str] = None
    allow_password_change: Optional[bool] = None
    avatar_file_id: Optional[int] = Field(default=None, foreign_key="files.id")
    phonenumber: Optional[str] = None
    user_type_id: Optional[int] = Field(default=None, foreign_key="user_types.id")
    bank_account_number: Optional[str] = None
    unioncard_number: Optional[str] = None
    institution: Optional[str] = None
    joined_in: Optional[int] = None
    confirmed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class User(UserBase, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    committee_memberships: list["CommitteeMember"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    news_items: list["NewsItem"] = Relationship(back_populates="creator", sa_relationship_kwargs={"foreign_keys": "[NewsItem.creator_id]"})
    comments: list["NewsComment"] = Relationship(back_populates="user")
    subscriptions: list["Subscription"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    mailing_list_memberships: list["MailingListMember"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    avatar_file: "File" = Relationship(sa_relationship_kwargs={"lazy": "selectin"})
    password: Optional[str] = None
    tokens: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    user_type: Optional["UserType"] = None
    avatar_file: Optional["File"] = None


################# USER TYPES

class UserTypeBase(SQLModel):
    id: int
    name_nl: Optional[str] = None
    name_en: Optional[str] = None
    is_donor: Optional[bool] = None
    is_competition: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserType(UserTypeBase, table=True):
    __tablename__ = "user_types"
    id: Optional[int] = Field(default=None, primary_key=True)

class UserTypeResponse(UserTypeBase):
    pass

######### PASSWORD ACTIONS

class ResetPasswordActionBase(SQLModel):
    id: int
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    token: Optional[str] = None
    sent_at: Optional[datetime] = None
    remember_created_at: Optional[datetime] = None

class ResetPasswordAction(ResetPasswordActionBase, table=True):
    __tablename__ = "reset_password_actions"
    id: Optional[int] = Field(default=None, primary_key=True)

class ResetPasswordActionResponse(ResetPasswordActionBase):
    pass
