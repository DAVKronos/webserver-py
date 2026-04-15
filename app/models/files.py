from typing import Optional
from sqlmodel import Field
from .base import TimestampModel

class FileBase(TimestampModel):
    file_name: str
    content_type: str
    file_size: int

class File(FileBase, table=True):
    __tablename__ = "files"

    id: Optional[int] = Field(default=None, primary_key=True)

class FileResponse(FileBase):
    id: int