from sqlmodel import Field, Relationship,  SQLModel
from datetime import datetime

class AnnouncementBase(SQLModel):
    id: int | None
    message: str | None
    title: str | None
    url: str | None
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