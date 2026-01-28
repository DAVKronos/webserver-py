
############### UPDATED #################
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

# Resolve circular imports
if TYPE_CHECKING:
    from .file import File

############## TAGS
class HasTag(SQLModel, table=True):
    __tablename__ = "has_tags"
    photo_id: int = Field(foreign_key="photos.id", primary_key=True)
    tag_id: int = Field(foreign_key="photo_tags.id", primary_key=True)

class PhotoTagBase(SQLModel):
    name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class PhotoTag(PhotoTagBase, table=True):
    __tablename__ = "photo_tags"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    photos: List["Photo"] = Relationship(back_populates="tags", link_model=HasTag)

class PhotoTagCreate(SQLModel):
    name: str

#################### PHOTO
class PhotoBase(SQLModel):
    file_id: Optional[int] = Field(default=None, foreign_key="files.id")
    photoalbum_id: Optional[int] = Field(default=None, foreign_key="photo_albums.id")
    exif_date: Optional[datetime] = None
    url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Photo(PhotoBase, table=True):
    __tablename__ = "photos"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships
    album: Optional["PhotoAlbum"] = Relationship(back_populates="photos")
    file: Optional["File"] = Relationship(sa_relationship_kwargs={"lazy": "selectin"})
    
    # Many-to-many relationship to tags
    tags: List[PhotoTag] = Relationship(back_populates="photos", link_model=HasTag)

class PhotoResponse(PhotoBase):
    id: int

class PhotoTagResponse(PhotoTagBase):
    id: int

################## PHOTO ALBUMS

class PhotoAlbumBase(SQLModel):
    id: int
    name_nl: Optional[str] = None
    name_en: Optional[str] = None
    agendaitem_id: Optional[int] = Field(default=None, foreign_key="agendaitems.id")
    is_public: Optional[bool] = False
    event_date: Optional[datetime] = None
    url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class PhotoAlbum(PhotoAlbumBase, table=True):
    __tablename__ = "photo_albums"
    id: Optional[int] = Field(default=None, primary_key=True)

    # Relationships
    photos: List[Photo] = Relationship(back_populates="album", sa_relationship_kwargs={"lazy": "selectin"})

class PhotoAlbumResponse(PhotoAlbumBase):
    pass

class PhotoAlbumUpdate(SQLModel):
    name_nl: Optional[str] = None
    name_en: Optional[str] = None
    event_date: Optional[str] = None
    url: Optional[str] = None
    is_public: Optional[bool] = None

PhotoAlbum.model_rebuild()
Photo.model_rebuild()
PhotoTag.model_rebuild()
HasTag.model_rebuild()