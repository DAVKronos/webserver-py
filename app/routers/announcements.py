from typing import Annotated
from datetime import datetime
from fastapi import APIRouter, Request, Depends, UploadFile
from sqlmodel import select
from ..dependencies import Database
from ..models.announcement import *

from datetime import datetime, timezone
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from pydantic import BaseModel, ValidationError
from sqlmodel import SQLModel, and_, func, select, text

from ..authentication import *
from ..dependencies import Database
from ..models.email.mailinglist import Mailinglist, MailinglistResponse
from ..models.email.alias import Alias, AliasResponse
from ..models.announcement import Announcement, AnnouncementResponse, AnnouncementUpdate, AnnouncementCreate

router = APIRouter(prefix="/announcements")

@router.get("", response_model=list[AnnouncementResponse])
async def index(r: Request, database: Database):
    query = select(Announcement)
    announcements = await database.exec(query)
    
    return announcements.all()

@router.get("/{id}", response_model=AnnouncementResponse)
async def get_article(id: int, database: Database):
    announcement = await database.get(Announcement, id)
    
    if announcement is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    return announcement

@router.post("", response_model=AnnouncementResponse)
async def create_announcement(data: AnnouncementCreate, backgound: UploadFile, database: Database, active_user: Annotated[User, Depends(current_user)]):
    print(data, backgound)
    t = datetime.utcnow()
    try:
        announcement = Announcement.model_validate(data, update={'created_at': t, 'updated_at': t, })
    except ValidationError as e:
        # log(e)
        print(e)
        raise HTTPException(status_code=500, detail="Input data not valid")
    
    database.add(announcement)
    await database.commit()
    await database.refresh(announcement)
     
    return announcement

@router.patch("/{id}", response_model=AnnouncementResponse)
async def update_announcement(id: int, data: AnnouncementUpdate, database: Database, active_user: Annotated[User, Depends(current_user)]):
    announcement = await database.get(Announcement, id)
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    t = datetime.utcnow()
    announcement_dict = data.model_dump(exclude_unset=True)
    announcement.sqlmodel_update(announcement, update = {'updated_at': t, **announcement_dict})
    database.add(announcement)

    await database.commit()
    await database.refresh(announcement)
    return announcement

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_announcement(id: int, database: Database, active_user: Annotated[User, Depends(current_user)]):
    announcement = await database.get(Announcement, id)

    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    await database.delete(announcement)
    await database.commit()
    return

@router.get("/current", response_model=list[AnnouncementResponse])
async def current(r: Request, database: Database):
    query = select(Announcement) \
        .order_by(Announcement.created_at.desc())
    
    announcements = await database.exec(query)

    moment = datetime.now()
    return [a for a in announcements if a.is_active_during(moment)]
