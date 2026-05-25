from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from .base import TimestampModel
from datetime import datetime

from .files import FileResponse
if TYPE_CHECKING:
    from .agendaitem import AgendaItem
    from .files import File


class HasTag(SQLModel, table=True):
    __tablename__ = "has_tag"

    photo_id: int = Field(foreign_key="photos.id", primary_key=True)
    tag_id: int = Field(foreign_key="photo_tags.id", primary_key=True)


class PhotoTagBase(TimestampModel):
    name: str


class PhotoTag(PhotoTagBase, table=True):
    __tablename__ = "photo_tags"
    id: Optional[int] = Field(default=None, primary_key=True)

    photos: List["Photo"] = Relationship(back_populates="tags", link_model=HasTag)


class PhotoTagResponse(PhotoTagBase):
    id: int


class PhotoBase(TimestampModel):
    file_id: int = Field(foreign_key="files.id")
    thumbnail_file_id = Field(foreign_key="files.id")
    photoalbum_id: int = Field(foreign_key="photo_albums.id")


class Photo(PhotoBase, table=True):
    __tablename__ = "photos"
    id: Optional[int] = Field(default=None, primary_key=True)

    album: "PhotoAlbum" = Relationship(back_populates="photos")
    tags: List[PhotoTag] = Relationship(back_populates="photos", link_model=HasTag)
    file: "File" = Relationship(sa_relationship_kwargs={'lazy': 'selectin'})
    thumbnail_file : "File" = Relationship(sa_relationship_kwargs={'lazy': 'selectin'})


class PhotoResponse(PhotoBase):
    id: int
    tags: List[PhotoTagResponse] = []
    file: "FileResponse"
    thumbnail_file: "FileResponse"

class PhotoAlbumBase(TimestampModel):
    name_nl: Optional[str] = None
    name_en: str
    is_public: Optional[bool] = True
    event_date: Optional[datetime] = None
    url: Optional[str] = None
    agendaitem_id: Optional[int] = Field(default=None, foreign_key="agendaitems.id")


class PhotoAlbum(PhotoAlbumBase, table=True):
    __tablename__ = "photo_albums"

    id: Optional[int] = Field(default=None, primary_key=True)
    agenda_item: Optional["AgendaItem"] = Relationship()
    photos: List["Photo"] = Relationship(back_populates="album")


class PhotoAlbumResponse(PhotoAlbumBase):
    id: int


class PhotoAlbumWithPhotosResponse(PhotoAlbumBase):
    id: int
    photos: List[PhotoResponse] = []


class PhotoAlbumUpdate(SQLModel):
    name_nl: Optional[str] = None
    name_en: Optional[str] = None
    event_date: Optional[str] = None
    url: Optional[str] = None
    is_public: Optional[bool] = None