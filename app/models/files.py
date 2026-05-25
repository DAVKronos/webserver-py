from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from .documents import Document

class FileBase(SQLModel):
    path: str
    content_type: str
    file_size: Optional[int] = None

class File(FileBase, table=True):
    __tablename__ = "files"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # relationship to Document
    documents: List["Document"] = Relationship(back_populates="file")


class FileResponse(FileBase):
    id: int