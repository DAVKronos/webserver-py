from fastapi import APIRouter, HTTPException
from sqlmodel import select

from ..dependencies import Database
from ..models.documents import Folder, Document
from ..models.files import File

router = APIRouter()

# -------------------------
# FOLDERS
# -------------------------

@router.get("/folders", response_model=list[Folder])
async def get_all_folders(database: Database):
    query = select(Folder).order_by(Folder.name.desc())
    result = await database.exec(query)
    return result.all()


@router.get("/folders/{id}", response_model=Folder)
async def get_one_folder(id: int, database: Database):
    folder = await database.get(Folder, id)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    return folder

@router.get("/folders/{id}/folders", response_model=list[Folder])
async def get_subfolders(id: int, database: Database):
    query = select(Folder).where(Folder.parent_folder_id == id)
    result = await database.exec(query)
    return result.all()


# -------------------------
# FILES 
# -------------------------

@router.get("/documents", response_model=list[File])
async def get_all_files(database: Database):
    query = select(File).order_by(File.file_name.desc())
    result = await database.exec(query)
    return result.all()



@router.get("/documents/{id}", response_model=File)
async def get_document_by_id(id: int, database: Database):
    query = select(File).where(File.id == id)
    result = await database.exec(query)
    file = result.first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    return file


# ✅ GET FILES BY FOLDER (via Document link table)
@router.get("/folders/{id}/documents", response_model=list[File])
async def get_files_by_folder(id: int, database: Database):
    query = (
        select(File)
        .join(Document, Document.file_id == File.id)
        .where(Document.folder_id == id)
        .order_by(File.file_name.desc())
    )

    result = await database.exec(query)
    return result.all()