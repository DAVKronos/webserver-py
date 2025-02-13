from sqlmodel import Field, Relationship,  SQLModel
from datetime import datetime
from .user import User, UserResponse

class CommentBase(SQLModel):
    created_at: datetime
    updated_at: datetime
    commenttext: str
    commentable_id: int
    commentable_type: str

class CommentPublic(CommentBase):
    user_id: int

class Comment(CommentBase, table=True):
    __tablename__: str = "comments"
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    user: User = Relationship(back_populates="comments", sa_relationship_kwargs={"lazy": "selectin"})
    
