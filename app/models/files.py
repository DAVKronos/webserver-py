from typing import Optional
from sqlmodel import Field, SQLModel
from .base import TimestampModel


class FileBase(TimestampModel):
    name: str
    content_type: str
    file_size: int
    folder_id: Optional[int] = None


class File(FileBase, table=True):
    __tablename__ = "files"

    id: Optional[int] = Field(default=None, primary_key=True)


class FileResponse(FileBase):
    id: int


# ---------------- FOLDER ----------------

class FolderBase(SQLModel):
    name: str


class Folder(FolderBase, table=True):
    __tablename__ = "document_folders"

    id: Optional[int] = Field(default=None, primary_key=True)


class FolderResponse(FolderBase):
    id: int