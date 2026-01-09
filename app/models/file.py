from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

class FileBase(SQLModel):
    id: int
    file_name: Optional[str] = None
    content_type: Optional[str] = None
    file_size: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class File(FileBase, table=True):
    __tablename__ = "files"
    id: Optional[int] = Field(default=None, primary_key=True)
    

class FileResponse(FileBase):
    pass