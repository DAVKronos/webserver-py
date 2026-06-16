from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from .base import TimestampModel
from datetime import date
from pydantic import BaseModel

from .files import FileResponse
if TYPE_CHECKING:
    from .files import File

class AnnouncementBase(TimestampModel):
    title: str
    content: str
    starts_at: Optional[date] = None
    ends_at: Optional[date] = None
    url: Optional[str] = None
    photo_file_id: Optional[int] = Field(default=None, foreign_key="files.id")

    def is_active_during(self, moment: date):
        return self.starts_at <= moment and self.ends_at >= moment

class Announcement(AnnouncementBase, table=True):
    __tablename__ = "announcements"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    photo_file: Optional["File"] = Relationship(sa_relationship_kwargs={'lazy': 'selectin'})

class AnnouncementResponse(AnnouncementBase):
    id: int
    photo_file: Optional["FileResponse"] = None

class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    starts_at: Optional[date] = None
    ends_at: Optional[date] = None
    url: Optional[str] = None
    photo_file_id: Optional[int] = None