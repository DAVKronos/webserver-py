from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class Folder(SQLModel, table=True):
    __tablename__ = "document_folders"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # relationship to Document
    documents: List["Document"] = Relationship(back_populates="folder")


class Document(SQLModel, table=True):
    __tablename__ = "documents"

    id: Optional[int] = Field(default=None, primary_key=True)

    file_id: int = Field(foreign_key="files.id")
    folder_id: int = Field(foreign_key="document_folders.id")

    # relationships
    file: Optional["File"] = Relationship(back_populates="documents")
    folder: Optional["Folder"] = Relationship(back_populates="documents")