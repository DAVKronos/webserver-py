from sqlmodel import Field, Relationship,  SQLModel
from datetime import datetime

class FileBase(SQLModel):
    id: int | None
    created_at: datetime | None
    updated_at: datetime | None
    folder_id: int | None
    public: bool | None
    name: str | None
    date: datetime | None
    file_file_name: str | None
    file_content_type: str | None
    file_file_size: int | None
    file_updated_at: datetime | None

class FileResponse(FileBase):
    pass

class File(FileBase, table=True):
    __tablename__: str = "kronometers"
    id: int | None = Field(default=None, primary_key=True)
    
class FolderBase(SQLModel):
    id: int | None
    name: str | None
    folder_id: int | None

class FolderResponse(FileBase):
    pass

class Folder(FolderBase, table=True):
    __tablename__: str = "folders"
    id: int | None = Field(default=None, primary_key=True)
    