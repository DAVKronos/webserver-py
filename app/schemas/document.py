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
    parent_folder_id: Optional[int] = None


class DocumentFolderResponse(DocumentFolderBase):
    pass

########## DOCUMENTS
class DocumentBase(SQLModel):
    name: Optional[str] = None
    date: Optional[str] = None # Should actually be date, but that causes an error with the name of the field
    file_id: Optional[int] = None
    folder_id: Optional[int] = None
    is_public: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class DocumentResponse(DocumentBase):
    id: int
