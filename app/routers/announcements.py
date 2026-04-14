from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Request, Depends
from sqlmodel import select
from ..dependencies import Database
from ..models.announcement import *

router = APIRouter(prefix="/announcements")

@router.get("/current", response_model=list[AnnouncementResponse])
async def current(r: Request, database: Database):
    query = select(Announcement) \
        .order_by(Announcement.created_at.desc())
    
    announcements = await database.exec(query)

    moment = datetime.now()
    return [a for a in announcements if a.is_active_during(moment)]
