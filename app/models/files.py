from typing import Optional
from sqlmodel import Field, SQLModel , Relationship
from .base import TimestampModel


class FileBase(SQLModel):
    file_name: str
    content_type: str
    file_size: int


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



class Document(SQLModel, table=True):
    __tablename__ = "documents"

    id: Optional[int] = Field(default=None, primary_key=True)

    file_id: int = Field(foreign_key="files.id")
    folder_id: int = Field(foreign_key="document_folders.id")

    file: Optional["File"] = Relationship()
    folder: Optional["Folder"] = Relationship()