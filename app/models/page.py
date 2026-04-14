from typing import Optional
from sqlmodel import Field
from .base import TimestampModel

class PageBase(TimestampModel):
    content_nl: Optional[str] = None
    content_en: Optional[str] = None
    page_title_nl: str
    page_title_en: str
    menu_item: Optional[str] = None
    is_highlight: bool = False
    is_public: bool = True

class Page(PageBase, table=True):
    __tablename__ = "pages"
    id: Optional[int] = Field(default=None, primary_key=True)

class PageResponse(PageBase):
    id: int