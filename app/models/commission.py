from sqlmodel import Field, Relationship,  SQLModel
from datetime import datetime
from .user import User, CompactUserResponse
from typing import Optional

class CommissionBase(SQLModel):
    id: int
    created_at: datetime
    updated_at: datetime
    name: str
    name_en: str
    description: str
    description_en: str
    email: Optional[str] = None
    role: Optional[str] = None

class CommissionResponse(CommissionBase):
    pass

class CompactCommissionResponse(SQLModel):
    name: str
    name_en: str

class Commission(CommissionBase, table=True):
    __tablename__: str = "commissions"
    id: int | None = Field(default=None, primary_key=True)
    commission_memberships: list["CommissionMembership"] = Relationship(back_populates="commission")

class CommissionCreate(SQLModel):
    name: str
    name_en: str
    description: str
    description_en: str

class ComissionUpdate(SQLModel):
    name: Optional[str] = None
    name_en: Optional[str] = None
    description: Optional[str] = None
    description_en: Optional[str] = None

class CommissionMembershipBase(SQLModel):
    id: int
    created_at: datetime
    updated_at: datetime
    function: str
    installed: bool

class CommissionMembership(CommissionMembershipBase, table=True):
    __tablename__: str ="commission_memberships"
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    user: User = Relationship(back_populates="commission_memberships", sa_relationship_kwargs={"lazy": "selectin"})
    commission_id: int = Field(foreign_key="commissions.id")
    commission: Commission = Relationship(back_populates="commission_memberships", sa_relationship_kwargs={"lazy": "selectin"})


class CommissionMembershipResponse(CommissionMembershipBase):
    user: CompactUserResponse
    commission: CompactCommissionResponse
    user: CompactUserResponse

class CommissionMembershipCreate(SQLModel):
    user_id: int
    function: str
