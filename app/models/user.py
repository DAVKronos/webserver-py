from sqlmodel import Field, Relationship,  SQLModel
from datetime import date, datetime
from typing import Optional

class UserBase(SQLModel):
    id: int
    name: str
    initials: str
    email: str
    birthdate: Optional[date]
    address: Optional[str]
    postalcode: Optional[str]
    city: Optional[str]
    sex: Optional[str]
    licensenumber: Optional[str]
    papieren_kronometer: Optional[bool]
    created_at: datetime
    updated_at: datetime
    avatar_file_name: Optional[str]
    avatar_content_type: Optional[str]
    avatar_file_size: Optional[int]
    avatar_updated_at: Optional[datetime]
    encrypted_password: str
    phonenumber: Optional[str]
    user_type_id: int
    xtracard: Optional[str]
    studie: Optional[str]
    instelling: Optional[str]
    aanvang: Optional[int]

class UserUpdate(SQLModel):
    name: Optional[str] = None
    initials: Optional[str] = None
    email: Optional[str] = None
    birthdate: Optional[date] = None
    address: Optional[str] = None
    postalcode: Optional[str] = None
    city: Optional[str] = None
    sex: Optional[str] = None
    licensenumber: Optional[str]
    papieren_kronometer: Optional[bool] 
    avatar_file_name: Optional[str] = None
    avatar_content_type: Optional[str] = None
    avatar_file_size: Optional[int] = None
    avatar_updated_at: Optional[datetime] = None
    phonenumber: Optional[str] = None
    xtracard: Optional[str] = None
    studie: Optional[str] = None
    instelling: Optional[str] = None
    aanvang: Optional[int] = None

class UserResponse(UserBase):
    commissions: list["CompactCommissionResponse"] = []
    
class User(UserBase, table=True):
    __tablename__: str = "users"
    id: int | None = Field(default=None, primary_key=True)
    articles: list["Article"] = Relationship(back_populates="user")
    comments: list["Comment"] = Relationship(back_populates="user")
    commission_memberships: list["CommissionMembership"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    subscriptions: list["Subscription"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    
    @property
    def commissions(self):
        return [
            CompactCommissionResponse(
                id=membership.commission.id,
                name=membership.commission.name,
                name_en=membership.commission.name_en
            ) 
            for membership in self.commission_memberships
        ]

class UserTypeBase(SQLModel):
    id: int
    name: str | None
    name_en: str | None
    donor: bool | None
    competition: bool | None
    

class UserTypeResponse(UserTypeBase):
    pass
    
class UserType(UserTypeBase, table=True):
    __tablename__: str = "user_types"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime
    updated_at: datetime

class CompactUserResponse(SQLModel):
    id: int
    name: str
    initials: str

from .commission import CompactCommissionResponse