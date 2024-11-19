from sqlmodel import Field, Relationship,  SQLModel
from datetime import datetime
from ..models.user import User
class CommissionBase(SQLModel):
    name: str

class Commission(CommissionBase, table=True):
    __tablename__: str = "commissions"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime
    updated_at: datetime
    name: str
    name_en:str
    description: str
    description_en: str
    email: str
    role: str
    commission_memberships: list["CommissionMembership"] = Relationship(back_populates="commission")

class CommissionMembershipBase(SQLModel):
    pass

class CommissionMembership(CommissionMembershipBase, table=True):
    __tablename__: str ="commission_memberships"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime
    updated_at: datetime
    user_id: int = Field(foreign_key="users.id")
    user: User = Relationship(back_populates="commission_memberships", sa_relationship_kwargs={"lazy": "selectin"})
    commission_id: int = Field(foreign_key="commissions.id")
    commission: Commission = Relationship(back_populates="commission_memberships", sa_relationship_kwargs={"lazy": "selectin"})
    function: str
    installed: bool
