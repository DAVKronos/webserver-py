from sqlmodel import Field, Relationship,  SQLModel
from datetime import date, datetime

class UserBase(SQLModel):
    name: str
    initials: str
    email: str
    birthdate: date | None
    created_at: datetime
    updated_at: datetime
    avatar_file_name: str | None
    avatar_content_type: str | None
    avatar_file_size: int | None
    avatar_updated_at: datetime | None
    user_type_id: int
    encrypted_password: str

class UserResponse(UserBase):
    id: int | None
    
class User(UserBase, table=True):
    __tablename__: str = "users"
    id: int | None = Field(default=None, primary_key=True)
    articles: list["Article"] = Relationship(back_populates="user")
    comments: list["Comment"] = Relationship(back_populates="user")
    commission_memberships: list["CommissionMembership"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    subscriptions: list["Subscription"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})


class UserTypeBase(SQLModel):
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