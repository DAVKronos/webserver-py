
############### UPDATED #################
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

# Resolve circular imports
if TYPE_CHECKING:
    from .file import File

############## TAGS
class PhotoTagBase(SQLModel):
    name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class PhotoTagCreate(SQLModel):
    name: str

#################### PHOTO
class PhotoBase(SQLModel):
    file_id: Optional[int] = None
    photoalbum_id: Optional[int] = None
    exif_date: Optional[datetime] = None
    url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class PhotoResponse(PhotoBase):
    id: int

class PhotoTagResponse(PhotoTagBase):
    id: int

################## PHOTO ALBUMS

class PhotoAlbumBase(SQLModel):
    id: int
    name_nl: Optional[str] = None
    name_en: Optional[str] = None
    agendaitem_id: Optional[int] = None
    is_public: Optional[bool] = False
    event_date: Optional[datetime] = None
    url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class PhotoAlbumResponse(PhotoAlbumBase):
    pass

class PhotoAlbumUpdate(SQLModel):
    name_nl: Optional[str] = None
    name_en: Optional[str] = None
    event_date: Optional[str] = None
    url: Optional[str] = None
    is_public: Optional[bool] = None