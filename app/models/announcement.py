from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from .base import TimestampModel
from datetime import datetime

from .files import FileResponse
if TYPE_CHECKING:
    from .files import File

class AnnouncementBase(TimestampModel):
    title: str
    content: str
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    url: Optional[str] = None
    photo_file_id: Optional[int] = Field(default=None, foreign_key="files.id")

    def is_active_during(self, moment: datetime):
        return self.starts_at <= moment and self.ends_at >= moment

class Announcement(AnnouncementBase, table=True):
    __tablename__ = "announcements"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    photo_file: Optional["File"] = Relationship()

class AnnouncementResponse(AnnouncementBase):
    id: int
    photo_file: Optional["FileResponse"]