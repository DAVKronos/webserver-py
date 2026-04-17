from fastapi import APIRouter, Request, HTTPException, Depends, status
from sqlalchemy.sql import extract
from sqlmodel import select, or_
from ..dependencies import Database
from datetime import date
from ..models.user import *
from ..models.committees import *
from typing import Annotated
from ..authentication import get_current_user

# All user endpoints need authentication
router = APIRouter(
    prefix="/users",
    # dependencies=[Depends(get_current_user)]
)

@router.get("", response_model=list[UserResponse])
async def get_all(r: Request, database: Database):
    query = select(User) \
        .order_by(User.name.asc())
    users = await database.exec(query)
    return users.all()

@router.get("/birthdays", response_model=list[UserResponse])
async def get_birthdays(r: Request, database: Database):
    today = date.today()
    next_month = (today.month % 12) + 1
    query = select(User).where(
        User.user_type_id != 9,
        User.birthdate.is_not(None),
        or_(
            (extract("month", User.birthdate) == today.month) & (extract("day", User.birthdate) >= today.day),
            (extract("month", User.birthdate) == next_month) & (extract("day", User.birthdate) <= today.day)
        )
    ).order_by(
        extract("month", User.birthdate),
        extract("day", User.birthdate)
    )
    users = await database.exec(query)
    return users.all()

@router.get("/{id}", response_model=UserResponse)
async def get_one(id: int, r: Request, database: Database):
    user= await database.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{id}")
async def delete_user(id: int, r: Request, database: Database):
    user = await database.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await database.delete(user)
    await database.commit()

@router.get("/{id}/committees", response_model=list[CommitteeResponse])
async def get_committees(id: int, r: Request, database: Database):
    user = await database.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.committees