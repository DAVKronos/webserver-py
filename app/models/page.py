from sqlmodel import Field, Relationship,  SQLModel
from datetime import datetime

class PageBase(SQLModel):
    id: int | None
    created_at: datetime | None
    updated_at: datetime | None
    public: bool | None
    highlight: bool | None
    sort_order: int | None
    information: str | None
    information_en: str | None
    pagetag: str | None
    pagetag_en: str | None
    menu: str | None

class PageResponse(PageBase):
    pass

class Page(PageBase, table=True):
    __tablename__: str = "pages"
    id: int | None = Field(default=None, primary_key=True)
