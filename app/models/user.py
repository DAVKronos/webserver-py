from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from .base import TimestampModel
from datetime import datetime, date

# This only runs during type checking, not at runtime
if TYPE_CHECKING:
    from .agenda import AgendaItem
    from .news import NewsItem

class User(TimestampModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    
    name: str
    initials: Optional[str] = None
    email: str = Field(unique=True, index=True)
    birthdate: Optional[date] = None
    address: Optional[str] = None
    postalcode: Optional[str] = None
    city: Optional[str] = None
    sex: Optional[str] = None
    allow_password_change: bool = True
    phonenumber: Optional[str] = None
    bank_account_number: Optional[str] = None
    unioncard_number: Optional[str] = None
    institution: Optional[str] = None
    joined_in: Optional[int] = None
    tokens: Optional[str] = None
    confirmed_at: Optional[datetime] = None
    password: str


    
    # Foreign Keys to tables not yet implemented
    avatar_file_id: Optional[int] = None
    user_type_id: Optional[int] = None

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

