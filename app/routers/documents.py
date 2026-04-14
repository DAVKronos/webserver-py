# from typing import Annotated
# from fastapi import APIRouter, Request, HTTPException
# from sqlmodel import select
# from ..dependencies import Database
# from ..models.document import *
# from ..models.file import *
# from ..schemas.document import *
# from ..schemas.file import *

# router = APIRouter(prefix="")

# @router.get("/folders", response_model=list[DocumentFolderResponse])
# async def get_all(r: Request, database: Database):
#     query = select(DocumentFolder) \
#         .order_by(DocumentFolder.name.desc())

#     folders = await database.exec(query)
#     return folders.all()

# @router.get("/folders/{id}", response_model=DocumentFolderResponse)
# async def get_one(id: int, r: Request, database: Database):
#     folder = await database.get(folder, id)
#     if not folder:
#         raise HTTPException(status_code=404, detail="DocumentFolder not found")
#     return folder

# @router.get("/kronometers", response_model=list[FileResponse])
# async def get_all_files(r: Request, database: Database):
#     query = select(File) \
#         .order_by(File.name.desc())

#     files = await database.exec(query)
#     return files.all()

# @router.get("/folders/{id}/kronometers", response_model=list[FileResponse])
# async def get_file(id: int, r: Request, database: Database):
#     query = select(File) \
#         .where(File.folder_id == id) \
#         .order_by(File.create_at.desc())
    
#     files = await database.exec(query)
#     return files.all()
