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

    def is_before_deadline(self):
        if subscriptiondeadline is None:
            return False
        else:
            return datetime.now() < self.subscriptiondeadline
    
class AgendaitemResponse(AgendaitemBase):
    agendaitemtype_id: int | None
    agendaitemtype: AgendaitemTypeResponse | None = None
    subscriptions: list["SubscriptionResponse"] = []

class Agendaitem(AgendaitemBase, table=True):
    __tablename__: str = "agendaitems"
    id: int | None = Field(default=None, primary_key=True)
    agendaitemtype_id: int | None = Field(default=None, foreign_key="agendaitemtypes.id")
    agendaitemtype: AgendaitemType = Relationship(back_populates="agendaitems", sa_relationship_kwargs={"lazy": "selectin"})
    subscriptions: list["Subscription"] = Relationship(back_populates="agendaitem",sa_relationship_kwargs={"lazy": "selectin"})

# Trick to deal with Pydantic circular dependencies
from .subscription import SubscriptionResponse