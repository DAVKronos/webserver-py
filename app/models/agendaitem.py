from typing import List, Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from .base import TimestampModel
from datetime import datetime
from sqlalchemy.orm import selectinload 

if TYPE_CHECKING:
    from .user import User
  
class AgendaItemBase(TimestampModel):
    name_nl: str
    name_en: str
    description_nl: Optional[str] = None
    description_en: Optional[str] = None
    date: datetime
    location: Optional[str] = None
    is_internal: Optional[bool] = False
    url: Optional[str] = None
    can_subscribe: Optional[bool] = False
    subscription_deadline: Optional[datetime] = None
    max_subscriptions: Optional[int] = None
    
    # These IDs are usually required when creating/viewing
    committee_id: Optional[int] = None
    agendaitem_type_id: Optional[int] = None

class AgendaItem(AgendaItemBase, table=True):
    __tablename__ = "agendaitems"

    id: Optional[int] = Field(default=None, primary_key=True)
    
    created_by_user_id: int = Field(foreign_key="users.id")

    # Relationships
    creator: "User" = Relationship(back_populates="created_agenda_items", sa_relationship_kwargs={'lazy': 'selectin'})
    subscriptions: List["Subscription"] = Relationship(back_populates="agenda_item", sa_relationship_kwargs={'lazy': 'selectin'})

class AgendaItemResponse(AgendaItemBase):
    id: int
    created_by_user_id: int
    subscriptions: List["SubscriptionResponse"] = []

class AgendaItemCreate(SQLModel):
    id: int
    name_nl: str
    name_en: str
    description_nl: str
    description_en: str
    date: datetime
    location: Optional[str]
    committee_id: Optional[int] = Field(default=None, foreign_key="committees.id")
    is_internal: bool
    url: Optional[str]
    can_subscribe: bool
    subscription_deadline: Optional[datetime] = None
    max_subscriptions: Optional[int] = None

class AgendaItemUpdate(SQLModel):
    id: int  
    name_nl: Optional[str] = None
    name_en: Optional[str] = None
    description_nl: Optional[str] = None
    description_en: Optional[str] = None
    date: Optional[datetime] = None
    location: Optional[str] = None
    committee_id: Optional[int] = None
    is_internal: Optional[bool] = None
    url: Optional[str] = None
    can_subscribe: Optional[bool] = None
    subscription_deadline: Optional[datetime] = None
    max_subscriptions: Optional[int] = None

###########################################################################

class AgendaItemTypeBase(TimestampModel):
    name_nl: str
    name_en: str

class AgendaItemType(AgendaItemTypeBase, table=True):
    __tablename__ = "agendaitem_types"

    id: Optional[int] = Field(default=None, primary_key=True)

class AgendaItemTypeResponse(AgendaItemTypeBase):
    id: int


#############################################################

class SubscriptionBase(TimestampModel):
    comment: Optional[str] = None
    user_id: int = Field(foreign_key="users.id")
    agendaitem_id: int = Field(foreign_key="agendaitems.id")

class Subscription(SubscriptionBase, table=True):
    __tablename__ = "subscriptions"
    
    id: Optional[int] = Field(default=None, primary_key=True)

    user: "User" = Relationship()
    agenda_item: "AgendaItem" = Relationship(back_populates="subscriptions")

class SubscriptionResponse(SubscriptionBase):
    id: int