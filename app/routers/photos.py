from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlmodel import select
from sqlalchemy import func
from sqlalchemy.orm import selectinload
from datetime import datetime, timezone
from ..time_utils import now
from pathlib import Path
from ..file_utils import store_file

from ..dependencies import Database
from ..models.photos import *
from ..models.files import File as FileModel

router = APIRouter(prefix="/photoalbums")

PHOTO_DIR = Path("static/photos")
PHOTO_DIR.mkdir(parents=True, exist_ok=True)


@router.get("", response_model=list[PhotoAlbumResponse])
async def get_all(database: Database):
    query = select(PhotoAlbum).order_by(PhotoAlbum.name_en.desc())
    result = await database.exec(query)
    photoalbums = result.all()

    for album in photoalbums:
        if album.is_public is None:
            album.is_public = True

    print(f"📂 Retrieved {len(photoalbums)} photo albums")
    return photoalbums


@router.get("/{id}", response_model=PhotoAlbumResponse)
async def get_one(id: int, database: Database):
    photoalbum = await database.get(PhotoAlbum, id)
    if not photoalbum:
        raise HTTPException(status_code=404, detail="PhotoAlbum not found")

    if photoalbum.is_public is None:
        photoalbum.is_public = True

    return photoalbum


@router.get("/{album_id}/photos", response_model=list[PhotoResponse])
async def get_photos(album_id: int, database: Database):
    try:
        query = (
            select(Photo)
            .where(Photo.photoalbum_id == album_id)
            .order_by(Photo.created_at.desc())
            .options(
                selectinload(Photo.tags),
                selectinload(Photo.file),
            )
        )
        result = await database.exec(query)
        return result.all()

    except Exception as e:
        print("Error fetching photos with tags:", str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch photos")





@router.post("/{album_id}/photos")
async def add_photo(
    album_id: int,
    database: Database,
    photo: UploadFile = File(...),
):  
    album = await database.get(PhotoAlbum, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Photo album not found")

    file = await store_file(database, file, PHOTO_DIR)
    t = now()
    new_photo = Photo(
            photoalbum_id=album_id,
            file_id=file.id,
            thumbnail_file_id=file.id,
            created_at=t,
            updated_at=t
        )
    database.add(new_photo)
    await database.commit()
    await database.refresh(new_photo)

    return new_photo
    


@router.post("/", response_model=PhotoAlbumResponse, status_code=status.HTTP_201_CREATED)
async def create_photoalbum(
    data: PhotoAlbumCreate,
    database: Database
):
    try:
        t = now()
        new_album = PhotoAlbum.model_validate(data, update={"created_at": t, "updated_at": t})

        if new_album.is_public is None:
            new_album.is_public = True

        database.add(new_album)
        await database.commit()
        await database.refresh(new_album)

        return new_album

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not create album: {e}")


@router.put("/{album_id}", response_model=PhotoAlbumResponse)
async def update_photoalbum(
    album_id: int,
    data: PhotoAlbumUpdate,
    database: Database,
):
    album = await database.get(PhotoAlbum, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="PhotoAlbum not found")

    try:
        album_update = PhotoAlbumUpdate(**data.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid update data: {e}")

    for key, value in album_update.dict(exclude_unset=True).items():
        setattr(album, key, value)

    album.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)

    if album.is_public is None:
        album.is_public = True

    database.add(album)
    await database.commit()
    await database.refresh(album)

    return album


@router.delete("/{album_id}")
async def delete_photoalbum(
    album_id: int,
    database: Database
):
    print(f"🗑️ Deleting photo album {album_id}")

    album = await database.get(PhotoAlbum, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Photo album not found")

    await database.delete(album)
    await database.commit()

    print("✅ Album deleted")
    return {"status": "success", "message": "Album deleted"}


@router.delete("/{album_id}/photos/{photo_id}")
async def delete_photo(
    album_id: int,
    photo_id: int,
    database: Database,
):
    try:
        result = await database.exec(select(Photo).where(Photo.id == photo_id))
        photo = result.one_or_none()

        if not photo:
            raise HTTPException(status_code=404, detail="Photo not found")

        if photo.photoalbum_id != album_id:
            raise HTTPException(status_code=400, detail="Photo does not belong to this album")

        await database.delete(photo)
        await database.commit()

        return {"status": "success", "message": "Photo deleted"}

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error deleting photo: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete photo")


@router.post("/{album_id}/{photo_id}/tags")
async def add_tag_to_photo(
    album_id: int,
    photo_id: int,
    payload: PhotoTag,
    database: Database
):
    print("▶️ Received payload:", payload)

    photo = await database.get(Photo, photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")

    if photo.photoalbum_id != album_id:
        raise HTTPException(status_code=400, detail="Photo does not belong to this album")

    query = select(PhotoTag).where(PhotoTag.name == payload.name)
    result = await database.exec(query)
    tag = result.one_or_none()

    if not tag:
        tag = PhotoTag(name=payload.name)
        database.add(tag)
        await database.commit()
        await database.refresh(tag)

    link_check = await database.exec(
        select(HasTag)
        .where(HasTag.photo_id == photo_id)
        .where(HasTag.tag_id == tag.id)
    )
    if link_check.one_or_none():
        raise HTTPException(status_code=400, detail="Tag already linked to photo")

    new_link = HasTag(photo_id=photo_id, tag_id=tag.id)
    database.add(new_link)
    await database.commit()

    return {"status": "success", "tag": tag.name}


@router.get("/photos/search", response_model=list[PhotoResponse])
async def search_photos_by_tag(tag: str, database: Database):
    try:
        print(f"🔎 Searching photos with tag like: {tag}")

        tag_pattern = f"%{tag.lower()}%"

        query = (
            select(Photo)
            .join(HasTag, Photo.id == HasTag.photo_id)
            .join(PhotoTag, PhotoTag.id == HasTag.tag_id)
            .where(func.lower(PhotoTag.name).like(tag_pattern))
            .distinct()
            .options(
                selectinload(Photo.tags),
                selectinload(Photo.file),
            )
        )

        result = await database.exec(query)
        photos = result.all()
        print(f"🔍 Found {len(photos)} matching photo(s)")
        return photos

    except Exception as e:
        print(f"❌ Error searching photos by tag '{tag}': {e}")
        raise HTTPException(status_code=500, detail="Failed to search photos")