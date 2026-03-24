############### UPDATED #################
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

# Resolve circular imports
if TYPE_CHECKING:
    from .file import File

class AnnouncementBase(SQLModel):
    id: int
    title: Optional[str] = None
    content: Optional[str] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    photo_file_id: Optional[int] = None
    url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def is_active_during(self, moment: datetime):
        return self.starts_at <= moment and self.ends_at >= moment

class AnnouncementResponse(AnnouncementBase):
    photo_file: Optional["File"] = None
