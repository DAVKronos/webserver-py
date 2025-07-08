from sqlmodel import Field, Relationship,  SQLModel
from datetime import datetime
from fastapi import File

class AnnouncementBase(SQLModel):
    id: int | None
    message: str | None
    title: str | None
    url: str | None
    background_file_name: str | None
    background_content_type: str | None
    starts_at: datetime | None
    ends_at: datetime | None

    def is_active_during(self, moment: datetime):
        return self.starts_at <= moment and self.ends_at >= moment

class Announcement(AnnouncementBase, table=True):
    __tablename__: str = "announcements"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime
    updated_at: datetime

class AnnouncementResponse(AnnouncementBase):
    pass

class AnnouncementUpdate(SQLModel):
    title: str | None
    message: str | None
    url: str | None
    starts_at: datetime | None
    ends_at: datetime | None

class AnnouncementCreate(SQLModel):
    title: str
    message: str
    url: str
    starts_at: datetime
    ends_at: datetime