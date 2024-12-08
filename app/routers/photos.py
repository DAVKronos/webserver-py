from typing import Annotated
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from ..dependencies import Database
from ..models.photo import *

router = APIRouter(prefix="/photoalbums")

@router.get("", response_model=list[PhotoalbumResponse])
async def get_all(r: Request, database: Database):
    query = select(Photoalbum) \
        .order_by(Photoalbum.name.desc())

    photoalbums = await database.exec(query)
    return photoalbums.all()

@router.get("/{id}", response_model=PhotoalbumResponse)
async def get_one(id: int, r: Request, database: Database):
    photoalbum = database.get(photoalbum, id)
    if not photoalbum:
        raise HTTPException(status_code=404, detail="Photoalbum not found")
    return photoalbum

@router.get("/{album_id}/photos", response_model=list[PhotoResponse])
async def get_photos(id: int, r: Request, database: Database):
    query = select(Photo) \
        .where(Photo.photoalbum_id == id) \
        .order_by(Photo.create_at.desc())
    
    photos = await database.exec(query)
    return photos.all()
