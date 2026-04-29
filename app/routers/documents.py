from fastapi import APIRouter, Request, HTTPException
from sqlmodel import select

from ..dependencies import Database
from ..models.document import Folder
from ..models.files import File

router = APIRouter()

# -------------------------
# FOLDERS
# -------------------------

@router.get("/folders", response_model=list[Folder])
async def get_all_folders(r: Request, database: Database):
    query = select(Folder).order_by(Folder.name.desc())
    folders = await database.exec(query)
    return folders.all()


@router.get("/folders/{id}", response_model=Folder)
async def get_one_folder(id: int, r: Request, database: Database):
    folder = await database.get(Folder, id)
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    return folder


# -------------------------
# FILES / KRONOMETERS
# -------------------------

@router.get("/kronometers", response_model=list[File])
async def get_all_files(r: Request, database: Database):
    query = select(File).order_by(File.name.desc())
    files = await database.exec(query)
    return files.all()


@router.get("/folders/{id}/kronometers", response_model=list[File])
async def get_files_by_folder(id: int, r: Request, database: Database):
    query = (
        select(File)
        .where(File.folder_id == id)
        .order_by(File.created_at.desc())
    )
    files = await database.exec(query)
    return files.all()