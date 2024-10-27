from sqlmodel import Field, Relationship,  SQLModel
from datetime import datetime
from ..models.agendaitem import Agendaitem
from ..models.user import User

class SubscriptionBase(SQLModel):
    name: str
    comment: str | None
    created_at: datetime
    updated_at: datetime
    reserve: bool

class SubscriptionResponse(SubscriptionBase):
    id: int | None


class Subscription(SubscriptionBase, table=True):
    __tablename__: str = "subscriptions"
    id: int | None = Field(default=None, primary_key=True)
    agendaitem_id: int = Field(foreign_key="agendaitems.id")
    agendaitem: Agendaitem = Relationship(back_populates="subscriptions", sa_relationship_kwargs={"lazy": "selectin"})
    user_id: int = Field(foreign_key="users.id")
    user: User = Relationship(back_populates="subscriptions", sa_relationship_kwargs={"lazy": "selectin"})
    
