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
from sqlalchemy import func


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
async def get_photos(album_id: int, database: Database):
    try:
        query = select(Photo).where(Photo.photoalbum_id == album_id).order_by(Photo.created_at.desc())
        result = await database.exec(query)
        photos = result.all()

        photo_responses = []

        for photo in photos:
            tag_links = await database.exec(
                select(PhotoTag, Tag)
                .join(Tag, Tag.id == PhotoTag.tag_id)
                .where(PhotoTag.photo_id == photo.id)
            )
            tag_names = [tag.name for _, tag in tag_links]

            # ✅ Construct proper PhotoResponse
            photo_response = PhotoResponse(
                id=photo.id,
                created_at=photo.created_at,
                updated_at=photo.updated_at,
                photoalbum_id=photo.photoalbum_id,
                processing=photo.processing,
                exif_date=photo.exif_date,
                youtube_id=photo.youtube_id,
                caption=photo.caption,
                photo_file_name=photo.photo_file_name,
                photo_content_type=photo.photo_content_type,
                photo_file_size=photo.photo_file_size,
                photo_updated_at=photo.photo_updated_at,
                photo_url_original=photo.photo_url_original,
                photo_url_thumb=photo.photo_url_thumb,
                tags=tag_names
            )
            photo_responses.append(photo_response)

        return photo_responses

    except Exception as e:
        print("Error fetching photos with tags:", str(e))
        raise HTTPException(status_code=500, detail="Failed to fetch photos")

    


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
    




class TagToPhotoPayload(SQLModel):
    tag: str  # name of the tag, e.g. "sunset"

class Tag(SQLModel, table=True):
    __tablename__ = "tag_"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
class PhotoTag(SQLModel, table=True):
    __tablename__ = "photo_tags"
    photo_id: int = Field(foreign_key="photos.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag_.id", primary_key=True)




@router.post("/{album_id}/{photo_id}/tags")
async def add_tag_to_photo(
    album_id: int,
    photo_id: int,
    payload: TagToPhotoPayload,
    database: Database
):
    print("▶️ Received payload:", payload)
    # Step 1: Check that the photo exists and belongs to the album
    photo = await database.get(Photo, photo_id)
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    if photo.photoalbum_id != album_id:
        raise HTTPException(status_code=400, detail="Photo does not belong to this album")

    # Step 2: Ensure tag exists in `tag_` table (create if not)
    query = select(Tag).where(Tag.name == payload.tag)
    result = await database.exec(query)
    tag = result.one_or_none()

    if not tag:
        tag = Tag(name=payload.tag)
        database.add(tag)
        await database.commit()
        await database.refresh(tag)

    # Step 3: Add entry to `photo_tags` if not already linked
    # Check if photo-tag link exists
    link_check = await database.exec(
        select(PhotoTag)
        .where(PhotoTag.photo_id == photo_id)
        .where(PhotoTag.tag_id == tag.id)
    )
    if link_check.one_or_none():
        raise HTTPException(status_code=400, detail="Tag already linked to photo")

    # Create new link
    new_link = PhotoTag(photo_id=photo_id, tag_id=tag.id)
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
            .join(PhotoTag, Photo.id == PhotoTag.photo_id)
            .join(Tag, Tag.id == PhotoTag.tag_id)
            .where(func.lower(Tag.name).like(tag_pattern))
            .distinct()
        )

        result = await database.exec(query)
        photos = result.all()
        print(f"🔍 Found {len(photos)} matching photo(s)")

        photo_responses = []

        for photo in photos:
            tag_links = await database.exec(
                select(PhotoTag, Tag)
                .join(Tag, Tag.id == PhotoTag.tag_id)
                .where(PhotoTag.photo_id == photo.id)
            )
            tag_names = [tag.name for _, tag in tag_links]

            photo_response = PhotoResponse(
                id=photo.id,
                created_at=photo.created_at,
                updated_at=photo.updated_at,
                photoalbum_id=photo.photoalbum_id,
                processing=photo.processing,
                exif_date=photo.exif_date,
                youtube_id=photo.youtube_id,
                caption=photo.caption,
                photo_file_name=photo.photo_file_name,
                photo_content_type=photo.photo_content_type,
                photo_file_size=photo.photo_file_size,
                photo_updated_at=photo.photo_updated_at,
                photo_url_original=photo.photo_url_original,
                photo_url_thumb=photo.photo_url_thumb,
                tags=tag_names
            )
            photo_responses.append(photo_response)

        return photo_responses

    except Exception as e:
        print(f"❌ Error searching photos by tag '{tag}': {e}")
        raise HTTPException(status_code=500, detail="Failed to search photos")
