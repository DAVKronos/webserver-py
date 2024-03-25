from typing import Annotated
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from ..database.pg import get_database
from ..queries import photos

router = APIRouter(prefix="/photoalbums")

@router.get("/", response_class=JSONResponse)
async def get(r: Request, database: Annotated[dict, Depends(get_database)]):
    res = await photos.get_albums(database)
    return res

@router.get("/{album_id}", response_class=JSONResponse)
async def get(album_id: int, r: Request, database: Annotated[dict, Depends(get_database)]):
    res = await photos.get_albums(database, album_id)
    return res

@router.get("/{album_id}/photos", response_class=JSONResponse)
async def get(album_id: int, r: Request, database: Annotated[dict, Depends(get_database)]):
    res = await photos.get(database, album_id)
    return res
