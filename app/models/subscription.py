from sqlmodel import Field, Relationship,  SQLModel
from datetime import datetime
from .agendaitem import Agendaitem

class SubscriptionBase(SQLModel):
    name: str
    comment: str | None
    created_at: datetime
    updated_at: datetime
    user_id: int | None
    reserve: bool

class SubscriptionResponse(SubscriptionBase):
    id: int | None


class Subscription(SubscriptionBase, table=True):
    __tablename__: str = "subscriptions"
    id: int | None = Field(default=None, primary_key=True)
    agendaitem_id: int = Field(foreign_key="agendaitems.id")
    agendaitem: Agendaitem = Relationship(back_populates="subscriptions", sa_relationship_kwargs={"lazy": "selectin"})
    

