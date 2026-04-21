from typing import Optional
from sqlmodel import SQLModel, Field
from .base import TimestampModel

class FileBase(TimestampModel):
    file_name: Optional[str] = None
    content_type: Optional[str] = None
    file_size: Optional[int] = None


class File(FileBase, table=True):
    __tablename__ = "files"
    id: Optional[int] = Field(default=None, primary_key=True)


class FileResponse(FileBase):
    id: int