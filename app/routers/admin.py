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

router = APIRouter()

@router.get("/mailinglists", response_model=list[MailinglistResponse])
async def index(r: Request, database: Database):
    query = select(Mailinglist)
    mailinglists = await database.exec(query)
    
    return mailinglists.all()

@router.get("/mailinglists/{id}", response_model=MailinglistResponse)
async def get_article(id: int, database: Database):
    mailinglist = await database.get(Mailinglist, id)
    
    if mailinglist is None:
        raise HTTPException(status_code=404, detail="Mailinglist not found")

    return mailinglist

@router.get("/aliases", response_model=list[AliasResponse])
async def index(r: Request, database: Database):
    query = select(Alias)
    mailinglists = await database.exec(query)
    
    return mailinglists.all()

@router.get("/aliases/{id}", response_model=AliasResponse)
async def get_article(id: int, database: Database):
    mailinglist = await database.get(Alias, id)
    
    if mailinglist is None:
        raise HTTPException(status_code=404, detail="Mailinglist not found")
    
    return mailinglist
