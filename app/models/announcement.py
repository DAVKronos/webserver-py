############### UPDATED #################
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

class AnnouncementBase(SQLModel):
    id: int
    title: Optional[str] = None
    content: Optional[str] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    photo_file_id: Optional[int] = Field(default=None, foreign_key="files.id")
    url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def is_active_during(self, moment: datetime):
        return self.starts_at <= moment and self.ends_at >= moment

class Announcement(AnnouncementBase, table=True):
    __tablename__ = "announcements"
    id: Optional[int] = Field(default=None, primary_key=True)
    photo_file: "File" = Relationship(sa_relationship_kwargs={"lazy": "selectin"})

class AnnouncementResponse(AnnouncementBase):
    pass