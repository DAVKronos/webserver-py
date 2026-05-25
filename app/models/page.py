from typing import Optional
from sqlmodel import Field, SQLModel
from .base import TimestampModel

class PageBase(TimestampModel):
    content_nl: Optional[str] = None
    content_en: Optional[str] = None
    page_title_nl: str
    page_title_en: str
    menu_item: Optional[str] = None
    is_highlight: Optional[bool] = False
    is_public: bool = True

class Page(PageBase, table=True):
    __tablename__ = "pages"
    id: Optional[int] = Field(default=None, primary_key=True)

class PageResponse(PageBase):
    id: int

class PageCreate(SQLModel):
    content_nl: str
    content_en: str
    page_title_nl: str
    page_title_en: str
    menu_item: Optional[str] = None
    is_highlight: bool = False
    is_public: bool = True

class PageUpdate(SQLModel):
    content_nl: Optional[str] = None
    content_en: Optional[str] = None
    page_title_nl: Optional[str] = None
    page_title_en: Optional[str] = None
    menu_item: Optional[str] = None
    is_highlight: Optional[bool] = None
    is_public: Optional[bool] = None