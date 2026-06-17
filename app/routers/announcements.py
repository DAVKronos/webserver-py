from datetime import date, datetime
from fastapi import APIRouter
from sqlmodel import select
from ..dependencies import Database
from ..models.announcement import *
from ..time_utils import now

router = APIRouter(prefix="/announcements")


# ----------------------------
# Helpers
# ----------------------------

def normalize_announcement(a: Announcement):
    # convert datetime -> date for output consistency
    if a.starts_at is not None and hasattr(a.starts_at, "date"):
        a.starts_at = a.starts_at.date()

    if a.ends_at is not None and hasattr(a.ends_at, "date"):
        a.ends_at = a.ends_at.date()

    return a


def to_naive_datetime(value):
    # fix timezone-aware -> naive mismatch with DB
    if isinstance(value, datetime) and value.tzinfo is not None:
        return value.replace(tzinfo=None)
    return value


# ----------------------------
# GET endpoints
# ----------------------------

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


# ----------------------------
# UPDATE
# ----------------------------

@router.patch("/{id}", response_model=AnnouncementResponse)
async def update_announcement(
    id: int,
    announcement_update: AnnouncementUpdate,
    database: Database
):
    announcement = await database.get(Announcement, id)

    if announcement is None:
        return None

    for key, value in announcement_update.model_dump(exclude_unset=True).items():
        setattr(announcement, key, to_naive_datetime(value))

    await database.commit()
    await database.refresh(announcement)

    return normalize_announcement(announcement)


# ----------------------------
# CREATE
# ----------------------------

@router.post("", response_model=AnnouncementResponse)
async def create_announcement(
    announcement_create: AnnouncementBase,
    database: Database
):
    t = now()

    data = announcement_create.model_dump()

    # important fix: avoid UTC vs naive DB crash
    if "starts_at" in data:
        data["starts_at"] = to_naive_datetime(data["starts_at"])

    if "ends_at" in data:
        data["ends_at"] = to_naive_datetime(data["ends_at"])

    announcement = Announcement.model_validate(
        data,
        update={
            "created_at": t,
            "updated_at": t,
        }
    )

    database.add(announcement)
    await database.commit()
    await database.refresh(announcement)

    return normalize_announcement(announcement)