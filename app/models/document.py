############### UPDATED #################
from typing import Optional, TYPE_CHECKING
from datetime import date, datetime
from sqlmodel import Field, SQLModel, Relationship

# Resolve circular imports
if TYPE_CHECKING:
    from .file import File

########## DOCUMENTS FOLDERS
class DocumentFolderBase(SQLModel):
    id: int
    name: Optional[str] = None
    parent_folder_id: Optional[int] = Field(default=None, foreign_key="document_folders.id")

class DocumentFolder(DocumentFolderBase, table=True):
    __tablename__ = "document_folders"
    id: Optional[int] = Field(default=None, primary_key=True)
    parent_folder: Optional["DocumentFolder"] = Relationship(back_populates="subfolders", sa_relationship_kwargs={"remote_side": "DocumentFolder.id"})
    subfolders: list["DocumentFolder"] = Relationship(back_populates="parent_folder")
    documents: list["Document"] = Relationship(back_populates="folder")

class DocumentFolderResponse(DocumentFolderBase):
    pass

########## DOCUMENTS
class DocumentBase(SQLModel):
    name: Optional[str] = None
    date: Optional[str] = None # Should actually be date, but that causes an error with the name of the field
    file_id: Optional[int] = Field(default=None, foreign_key="files.id")
    folder_id: Optional[int] = Field(default=None, foreign_key="document_folders.id")
    is_public: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Document(DocumentBase, table=True):
    __tablename__ = "documents"
    id: Optional[int] = Field(default=None, primary_key=True)
    folder: Optional[DocumentFolder] = Relationship(back_populates="documents")
    file: Optional["File"] = Relationship(sa_relationship_kwargs={"lazy": "selectin"})

class DocumentResponse(DocumentBase):
    id: int

DocumentFolder.model_rebuild()
Document.model_rebuild()