############### UPDATED #################
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

# Resolve circular imports
if TYPE_CHECKING:
    from .user import User
    from .agendaitem import AgendaItemType
    from .committee import Committee

############ AGENDA ITEMS
class AgendaItemBase(SQLModel):
    id: int
    name_nl: Optional[str] = None
    name_en: Optional[str] = None
    description_nl: Optional[str] = None
    description_en: Optional[str] = None
    date: Optional[datetime] = None
    location: Optional[str] = None
    committee_id: Optional[int] = Field(default=None, foreign_key="committees.id")
    is_internal: Optional[bool] = None
    agendaitem_type_id: Optional[int] = Field(default=None, foreign_key="agendaitem_types.id")
    url: Optional[str] = None
    created_by_user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    can_subscribe: Optional[bool] = None
    subscription_deadline: Optional[datetime] = None
    max_subscriptions: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def is_before_deadline(self):
        if self.subscription_deadline is None:
            return False
        else:
            return datetime.now() < self.subscription_deadline

class AgendaItem(AgendaItemBase, table=True):
    __tablename__ = "agendaitems"
    id: Optional[int] = Field(default=None, primary_key=True)
    subscriptions: list["Subscription"] = Relationship(back_populates="agendaitem",sa_relationship_kwargs={"lazy": "selectin"})
    created_by: "User" = Relationship(sa_relationship_kwargs={"lazy": "selectin"})
    agendaitem_type: "AgendaItemType" = Relationship(sa_relationship_kwargs={"lazy": "selectin"})
    committee: "Committee" = Relationship(sa_relationship_kwargs={"lazy": "selectin"})

class AgendaItemResponse(AgendaItemBase):
    subscriptions: Optional[list["Subscription"]] = None
    agendaitem_type: Optional["AgendaItemType"] = None
    created_by: Optional["User"] = None
    committee: Optional["Committee"] = None

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
    id: int  # Required to identify the record
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

############ AGENDA ITEM TYPES

class AgendaItemTypeBase(SQLModel):
    id: int
    name_nl: Optional[str] = None
    name_en: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class AgendaItemType(AgendaItemTypeBase, table=True):
    __tablename__ = "agendaitem_types"
    id: Optional[int] = Field(default=None, primary_key=True)

class AgendaItemTypeResponse(AgendaItemTypeBase):
    pass

############# SUBSCRIPTIONS

class SubscriptionBase(SQLModel):
    id: int
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    agendaitem_id: Optional[int] = Field(default=None, foreign_key="agendaitems.id")
    comment: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Subscription(SubscriptionBase, table=True):
    __tablename__ = "subscriptions"
    id: Optional[int] = Field(default=None, primary_key=True)
    agendaitem: "AgendaItem" = Relationship(back_populates="subscriptions",sa_relationship_kwargs={"lazy": "selectin"})
    user: "User" = Relationship(back_populates="subscriptions",sa_relationship_kwargs={"lazy": "selectin"})

class SubscriptionResponse(SubscriptionBase):
    pass

Subscription.model_rebuild()
AgendaItem.model_rebuild()
AgendaItemType.model_rebuild()