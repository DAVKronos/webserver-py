from typing import Annotated
from fastapi import APIRouter, Request, Depends, HTTPException, UploadFile, File, Body, Form
from sqlmodel import select
from ..dependencies import Database
from ..models.photo import *
from datetime import datetime, timezone
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession
import hashlib
import os
from starlette.status import HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED
from pathlib import Path
router = APIRouter(prefix="/photoalbums")

PHOTO_DIR = Path("static/photos")
PHOTO_DIR.mkdir(parents=True, exist_ok=True)

@router.get("", response_model=list[PhotoalbumResponse])
async def get_all(r: Request, database: Database):
    query = select(Photoalbum).order_by(Photoalbum.name.desc())
    photoalbums = await database.exec(query)  # Ensure async execution
    return photoalbums.all()

@router.get("/{id}", response_model=PhotoalbumResponse)
async def get_one(id: int, r: Request, database: Database):
    photoalbum = await database.get(Photoalbum, id)  # Fixed model reference
    if not photoalbum:
        raise HTTPException(status_code=404, detail="Photoalbum not found")
    return photoalbum

@router.get("/{album_id}/photos", response_model=list[PhotoResponse])
async def get_photos(album_id: int, r: Request, database: Database):
    try:
        query = select(Photo).where(Photo.photoalbum_id == album_id).order_by(Photo.created_at.desc())
        photos = await database.exec(query)
        if photos is None:
            raise HTTPException(status_code=500, detail="Database query failed")

        photos_list = photos.all()
        print(f"📸 Found {len(photos_list)} photos in album {album_id}")

        return photos_list

    except Exception as e:
        print(f"Error fetching photos2: {str(e)}")  # Logs error
        raise HTTPException(status_code=500, detail="Internal Server Error, Error fetching photos")
    


def generate_unique_filename(upload_file: UploadFile) -> str:
    original_name = upload_file.filename
    timestamp = datetime.utcnow().isoformat()
    hash_input = f"{original_name}-{timestamp}".encode()
    hashed = hashlib.sha1(hash_input).hexdigest()
    extension = os.path.splitext(original_name)[1]
    return f"{hashed}{extension}"


@router.post("/{album_id}/photos")
async def add_photo(
    album_id: int,
    database: Database,
    caption: str = Form(None, alias="photo[caption]"),
    photo: UploadFile = File(..., alias="photo[photo]"),
):
    print(f"📸 Uploading photo to album {album_id}")
    print(f"📸 Received photo upload for album {album_id}: {photo.filename}")

    try:
        # Generate unique file name and save to disk
        filename = generate_unique_filename(photo)
        file_path = PHOTO_DIR / filename

        with open(file_path, "wb") as f:
            f.write(await photo.read())

        photo_url = f"/static/photos/{filename}"

        # Save record in DB
        new_photo = Photo(
            photoalbum_id=album_id,
            photo_file_name=filename,
            photo_content_type=photo.content_type,
            caption=caption,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            processing=False,
            photo_url_original=photo_url,
            photo_url_thumb=photo_url
        )

        database.add(new_photo)
        await database.commit()
        await database.refresh(new_photo)

        print("✅ Photo uploaded and saved to DB")

        return {
            "id": new_photo.id,
            "filename": filename,
            "url": photo_url,
            "caption": new_photo.caption
        }

    except Exception as e:
        print(f"❌ Error uploading photo: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload photo")


@router.post("/", response_model=PhotoalbumResponse, status_code=status.HTTP_201_CREATED)
async def create_photoalbum(
    data: Photoalbum,
    database: Database
):
    try:
        album_data = data.dict()
        print("📥 Received create payload:", album_data)

        new_album = Photoalbum(
            **data.dict(exclude_unset=True),
            created_at=datetime.now(timezone.utc).replace(tzinfo=None),
            updated_at=datetime.now(timezone.utc).replace(tzinfo=None)
        )

        print("🛠 Creating album with data:", new_album.dict())

        database.add(new_album)
        await database.commit()
        await database.refresh(new_album)

        print("✅ Album created with ID:", new_album.id)
        return new_album

    except Exception as e:
        print("❌ Exception while creating album:", e)
        raise HTTPException(status_code=400, detail=f"Could not create album: {e}")

    

@router.put("/{album_id}", response_model=PhotoalbumResponse)
async def update_photoalbum(
    album_id: int,
    data: PhotoalbumUpdate,
    database: Database,
):
    print("hoi")
    print(data.dict())

    album = await database.get(Photoalbum, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Photoalbum not found")

    try:
        # Create update model from parsed Pydantic model
        album_update = PhotoalbumUpdate(**data.dict())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid update data: {e}")

    # Apply updated fields
    for key, value in album_update.dict(exclude_unset=True).items():
        setattr(album, key, value)

    database.add(album)
    await database.commit()
    await database.refresh(album)

    print("finished")
    return album




@router.delete("/{album_id}")
async def delete_photoalbum(
    album_id: int,
    database: Database
):
    print(f"🗑️ Deleting photo album {album_id}")

    album = await database.get(Photoalbum, album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Photo album not found")

    # Optionally delete related photos if needed
    # photos = await database.exec(select(Photo).where(Photo.photoalbum_id == album_id))
    # for photo in photos:
    #     await database.delete(photo)

    await database.delete(album)
    await database.commit()

    print("✅ Album deleted")
    return {"status": "success", "message": "Album deleted"}



@router.delete("/{album_id}/photos/{photo_id}")
async def delete_photo(
    album_id: int,
    database: Database,
    photo_id: int
):


    try:
        # Fetch the photo by ID
        result = await database.execute(select(Photo).where(Photo.id == photo_id))
        photo = result.scalar_one_or_none()

        if not photo:
            raise HTTPException(status_code=404, detail="Photo not found")

        if photo.photoalbum_id != album_id:
            raise HTTPException(status_code=400, detail="Photo does not belong to this album")

        # Delete image file from disk
        file_path = PHOTO_DIR / photo.photo_file_name
        if file_path.exists():
            file_path.unlink()
            print(f"🗑️ Deleted file: {file_path}")
        else:
            print(f"⚠️ File not found on disk: {file_path}")

        # Delete from database
        await database.delete(photo)
        await database.commit()

        return { "status": "success", "message": "Photo deleted" }

    except Exception as e:
        print(f"❌ Error deleting photo: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete photo")