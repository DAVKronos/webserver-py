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
 

class FileResponse(FileBase):
    pass
