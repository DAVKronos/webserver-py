from fastapi import APIRouter, Request, HTTPException
from sqlalchemy.sql import extract
from sqlmodel import select, or_
from ..dependencies import Database
from datetime import date
from ..models.user import *

router = APIRouter(prefix="/users")

@router.get("", response_model=list[UserResponse])
async def get_all(r: Request, database: Database):
    query = select(User) \
        .order_by(User.name.asc())
        #The users table currently has 2 problematic entries, id 479 & 340
        # these have a birthdate with the year 0001 initially gave return errors
        # after manually changing it and setting it back it somehow works again
        # but maybe update 01/01/0001 dates?
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
    user = await database.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user