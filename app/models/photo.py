from sqlmodel import Field, Relationship,  SQLModel
from datetime import datetime

class PhotoBase(SQLModel):
    id: int | None
    created_at: datetime | None
    updated_at: datetime | None
    photoalbum_id: int | None
    processing: bool | None
    exif_date: datetime | None
    youtube_id: str | None
    caption: str | None
    photo_file_name: str | None
    photo_content_type: str | None
    photo_file_size: int | None
    photo_updated_at: datetime | None
    photo_url_original: str | None
    photo_url_thumb: str | None

class PhotoResponse(PhotoBase):
    pass

class Photo(PhotoBase, table=True):
    __tablename__: str = "photos"
    id: int | None = Field(default=None, primary_key=True)


class PhotoalbumBase(SQLModel):
    id: int | None
    created_at: datetime | None
    updated_at: datetime | None
    agendaitem_id: int | None
    public: bool | None
    name: str | None
    name_en: str | None
    eventdate: datetime | None
    url: str | None

class PhotoalbumResponse(PhotoalbumBase):
    pass

class Photoalbum(PhotoalbumBase, table=True):
    __tablename__: str = "photoalbums"
    id: int | None = Field(default=None, primary_key=True)
