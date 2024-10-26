from sqlmodel import Field, Relationship,  SQLModel
from datetime import datetime

class UserBase(SQLModel):
    name: str

class UserPublic(UserBase):
    id: int | None
    email: str
    
class User(UserBase, table=True):
    __tablename__: str = "users"
    
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime
    updated_at: datetime
    user_type_id: int
    name: str
    initials: str
    email: str
    encrypted_password: str
    articles: list["Article"] = Relationship(back_populates="user")
    comments: list["Comment"] = Relationship(back_populates="user")

