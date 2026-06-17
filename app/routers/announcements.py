from datetime import date, datetime
from fastapi import APIRouter
from sqlmodel import select
from ..dependencies import Database
from ..models.announcement import *

router = APIRouter(prefix="/announcements")


# helper: FIX datetime -> date mismatch
def normalize_announcement(a: Announcement):
    if a.starts_at is not None:
        if hasattr(a.starts_at, "date"):
            a.starts_at = a.starts_at.date()

    if a.ends_at is not None:
        if hasattr(a.ends_at, "date"):
            a.ends_at = a.ends_at.date()

    return a


# 🔥 NEW: fix timezone mismatch (ONLY for this endpoint)
def to_naive_datetime(value):
    if isinstance(value, datetime) and value.tzinfo is not None:
        return value.replace(tzinfo=None)
    return value


@router.get("/current", response_model=list[AnnouncementResponse])
async def current(database: Database):
    query = select(Announcement).order_by(Announcement.created_at.desc())
    announcements = await database.exec(query)

    moment = date.today()

    result = []
    for a in announcements:
        a = normalize_announcement(a)
        if a.is_active_during(moment):
            result.append(a)

    return result


@router.get("", response_model=list[AnnouncementResponse])
async def all_announcements(database: Database):
    query = select(Announcement).order_by(Announcement.created_at.desc())
    announcements = await database.exec(query)

    return [normalize_announcement(a) for a in announcements]


@router.get("/{id}", response_model=AnnouncementResponse)
async def get_announcement(id: int, database: Database):
    query = select(Announcement).where(Announcement.id == id)

    result = await database.exec(query)
    announcement = result.one_or_none()

    if not announcement:
        return None

    return normalize_announcement(announcement)


@router.patch("/{id}", response_model=AnnouncementResponse)
async def update_announcement(
    id: int,
    announcement_update: AnnouncementUpdate,
    database: Database
):
    announcement = await database.get(Announcement, id)

    if announcement is None:
        return None

    # 🔥 FIX applied here
    for key, value in announcement_update.model_dump(exclude_unset=True).items():
        setattr(announcement, key, to_naive_datetime(value))

    await database.commit()
    await database.refresh(announcement)

    return normalize_announcement(announcement)