############### UPDATED #################
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

class PageBase(SQLModel):
    id: int
    content_nl: Optional[str] = None
    content_en: Optional[str] = None
    page_title_nl: Optional[str] = None
    page_title_en: Optional[str] = None
    menu_item: Optional[str] = None
    is_highlight: Optional[bool] = False
    is_public: Optional[bool] = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class PageResponse(PageBase):
    pass
