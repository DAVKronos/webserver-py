############### UPDATED #################
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

# Resolve circular imports
if TYPE_CHECKING:
    from .file import FileResponse
    from .user import UserResponse

################### NEWS COMMENT
class NewsCommentBase(SQLModel):
    id: int
    user_id: Optional[int] = None
    newsitem_id: Optional[int] = None
    content: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class NewsCommentPublic(NewsCommentBase):
    user: Optional["UserResponse"] = None

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
    photo_file_id: Optional[int] = None
    approved: Optional[bool] = False
    approved_by: Optional[int] = None
    creator_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

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
    approver: Optional["UserResponse"] = None
    comments: list["NewsCommentResponse"] = None

