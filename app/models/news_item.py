############### UPDATED #################
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

# Resolve circular imports
if TYPE_CHECKING:
    from .file import File, FileResponse
    from .user import UserResponse, User

################### NEWS COMMENT
class NewsCommentBase(SQLModel):
    id: int
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    newsitem_id: Optional[int] = Field(default=None, foreign_key="news_items.id")
    content: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class NewsComment(NewsCommentBase, table=True):
    __tablename__ = "news_comments"
    id: Optional[int] = Field(default=None, primary_key=True)
    user: "User" = Relationship(back_populates="comments", sa_relationship_kwargs={"lazy": "selectin"})

######## NEWS ITEMS
class NewsItemBase(SQLModel):
    id: int
    title_nl: Optional[str] = None
    title_en: Optional[str] = None
    content_nl: Optional[str] = None
    content_en: Optional[str] = None
    photo_file_id: Optional[int] = Field(default=None, foreign_key="files.id")
    approved: Optional[bool] = False
    approved_by: Optional[int] = Field(default=None, foreign_key="users.id")
    creator_id: Optional[int] = Field(default=None, foreign_key="users.id")
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class NewsItem(NewsItemBase, table=True):
    __tablename__ = "news_items"
    id: Optional[int] = Field(default=None, primary_key=True)
    creator: "User" = Relationship(back_populates="news_items", sa_relationship_kwargs={"lazy": "selectin", "foreign_keys": "[NewsItem.creator_id]"})
    approver: Optional["User"] = Relationship(sa_relationship_kwargs={"lazy": "selectin", "foreign_keys": "[NewsItem.approved_by]"})
    comments: list["NewsComment"] = Relationship(sa_relationship_kwargs = {"lazy": "selectin" })
    photo_file: "File" = Relationship(sa_relationship_kwargs={"lazy": "selectin"})
    

