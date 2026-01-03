from sqlmodel import Field, Relationship,  SQLModel
from datetime import datetime
from typing import Optional

class PageBase(SQLModel):
    id: int | None

    content_nl: Optional[str] = None
    content_en: Optional[str] = None

    page_title_nl: Optional[str] = None
    page_title_en: Optional[str] = None

    menu_item: Optional[str] = None

    is_highlight: Optional[bool] = None
    is_public: Optional[bool] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class PageResponse(PageBase):
    pass

class PageUpdate(SQLModel):
    public: bool | None
    highlight: bool | None
    sort_order: int | None
    information: str | None
    information_en: str | None
    pagetag: str | None
    pagetag_en: str | None
    menu: str | None

class PageCreate(SQLModel):
    public: bool = False
    highlight: bool = False
    sort_order: int | None = None
    information: str
    information_en: str
    pagetag: str
    pagetag_en: str
    menu: str

class Page(PageBase, table=True):
    __tablename__: str = "pages"
    id: int | None = Field(default=None, primary_key=True)
