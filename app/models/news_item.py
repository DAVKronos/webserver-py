from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from .base import TimestampModel

# Put all model imports outside the if statement
from .user import UserResponse
if TYPE_CHECKING:
    # Put all scheme (table) import in the if statement
    from .user import User

class NewsItemBase(TimestampModel):
    title_nl: str
    title_en: str
    content_nl: str
    content_en: str
    approved: bool = False
    photo_file_id: Optional[int] = None

    

class NewsItem(NewsItemBase, table=True):
    __tablename__ = "news_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Foreign Keys
    creator_id: Optional[int] = Field(foreign_key="users.id")
    approved_by: Optional[int] = Field(default=None, foreign_key="users.id")

    # Relationships
    comments: List["NewsComment"] = Relationship(back_populates="news_item", sa_relationship_kwargs={'lazy': 'selectin'})
    creator: "User" = Relationship(
        back_populates="created_news_items",
        sa_relationship_kwargs={"foreign_keys": "[NewsItem.creator_id]", 'lazy': 'selectin'}
    )
    approver: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[NewsItem.approved_by]", 'lazy': 'selectin'}
    )

class NewsItemPublicResponse(NewsItemBase):
    id: int

class NewsItemExtendedResponse(NewsItemPublicResponse):
    creator: Optional["UserResponse"] = None
    comments: List["NewsCommentResponse"] = None
    approved_by: Optional[int] = None
    


class NewsItemUpdate(SQLModel):
    title_nl: Optional[str] = None
    title_en: Optional[str] = None
    content_nl: Optional[str] = None
    content_en: Optional[str] = None

class NewsItemCreate(SQLModel):
    title_nl: str
    title_en: str
    content_nl: str
    content_en: str

class NewsCommentCreate(SQLModel):
    newsitem_id: int
    content: str
 
###############################################################

class NewsCommentBase(TimestampModel):
    content: str
    user_id: int = Field(foreign_key="users.id")
    newsitem_id: int = Field(foreign_key="news_items.id")

class NewsComment(NewsCommentBase, table=True):
    __tablename__ = "news_comments"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationships
    user: "User" = Relationship(sa_relationship_kwargs={'lazy': 'selectin'})
    news_item: "NewsItem" = Relationship(back_populates="comments")

class NewsCommentResponse(NewsCommentBase):
    id: int
    user: "UserResponse"