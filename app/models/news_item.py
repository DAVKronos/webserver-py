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

class NewsCommentPublic(NewsCommentBase):
    user: Optional["UserResponse"] = None

class NewsComment(NewsCommentBase, table=True):
    __tablename__ = "news_comments"
    id: Optional[int] = Field(default=None, primary_key=True)
    user: "User" = Relationship(back_populates="comments", sa_relationship_kwargs={"lazy": "selectin"})

class NewsCommentResponse(NewsCommentBase):
    pass

class NewsCommentCreate(SQLModel):
    newsitem_id: int
    content: str

class NewsCommentUpdate(SQLModel): 
    content: Optional[str] = None

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
    
    
class NewsItemCreate(SQLModel):
    title_nl: str
    title_en: str
    content_nl: str
    content_en: str

class NewsItemUpdate(SQLModel):
    title_nl: Optional[str]
    title_en: Optional[str]
    content_nl: Optional[str]
    content_en: Optional[str]

class NewsItemUpdate(SQLModel):
    title_nl: str | None = None
    title_en: str | None = None
    content_nl: str | None = None
    content_en: str | None = None


class NewsItemResponse(NewsItemBase):
    photo_file: Optional["FileResponse"] = None

class NewsItemPublicResponse(NewsItemResponse):
    creator: Optional["UserResponse"] = None
    approver: Optional["User"] = None
    comments: list["NewsComment"] = None

