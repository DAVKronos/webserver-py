from fastapi import APIRouter, Request, HTTPException
from sqlmodel import select

from ..dependencies import Database
from ..models.files import File, Folder

router = APIRouter()

# ---------------- FOLDERS ----------------

@router.get("/folders")
async def get_all_folders(database: Database):
    query = select(Folder).order_by(Folder.name.desc())
    result = await database.exec(query)
    return result.all()


@router.get("/folders/{id}")
async def get_folder(id: int, database: Database):
    folder = await database.get(Folder, id)

    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")

    return folder


# ---------------- FILES ----------------

@router.get("/kronometers")
async def get_all_files(database: Database):
    query = select(File).order_by(File.file_name.desc())
    result = await database.exec(query)
    return result.all()


@router.get("/folders/{id}/kronometers")
async def get_files_by_folder(id: int, database: Database):
    query = (
        select(File)
        .where(File.folder_id == id)
        .order_by(File.created_at.desc())
    )
    result = await database.exec(query)
    return result.all()