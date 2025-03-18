from sqlmodel import Field, Relationship,  SQLModel
from datetime import datetime
from .agendaitemtype import AgendaitemType, AgendaitemTypeResponse


class AgendaitemBase(SQLModel):
    id: int
    name: str | None
    description: str | None
    date: datetime | None
    location: str | None
    subscribe: bool | None
    subscriptiondeadline: datetime | None
    commission_id: int | None
    created_at: datetime | None
    updated_at: datetime | None
    category: str | None
    intern: bool | None
    url: str | None
    user_id: int | None
    name_en: str | None
    description_en: str | None
    maxsubscription: int | None
    agendaitemtype_id: int

    def is_before_deadline(self):
        if self.subscriptiondeadline is None:
            return False
        else:
            return datetime.now() < self.subscriptiondeadline
    
class AgendaitemResponse(AgendaitemBase):
    agendaitemtype: AgendaitemTypeResponse | None = None
    subscriptions: list["SubscriptionResponse"] = []

class Agendaitem(AgendaitemBase, table=True):
    __tablename__: str = "agendaitems"
    id: int | None = Field(default=None, primary_key=True)
    agendaitemtype_id: int | None = Field(default=None, foreign_key="agendaitemtypes.id")
    agendaitemtype: AgendaitemType = Relationship(back_populates="agendaitems", sa_relationship_kwargs={"lazy": "selectin"})
    subscriptions: list["Subscription"] = Relationship(back_populates="agendaitem",sa_relationship_kwargs={"lazy": "selectin"})



class AgendaItemCreate(SQLModel) :
    name: str 
    name_en: str 
    description: str 
    description_en: str 
    date: datetime 
    location: str | None
    commission_id: int | None
    category: str | None 
    intern: bool 
    agendaitemtype_id: int
    url: str | None
    subscribe: bool 
    subscriptiondeadline: datetime | None
    maxsubscription: int | None


class AgendaItemUpdate(SQLModel) :
    name: str | None
    name_en: str  | None
    description: str  | None
    description_en: str  | None
    date: datetime  | None
    location: str | None
    commission_id: int | None
    category: str | None 
    intern: bool | None
    agendaitemtype_id: int | None
    url: str | None
    subscribe: bool | None
    subscriptiondeadline: datetime | None
    maxsubscription: int | None
    




# Trick to deal with Pydantic circular dependencies
from .subscription import SubscriptionResponse