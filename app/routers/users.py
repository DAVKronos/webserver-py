from typing import Annotated
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlmodel import select
from ..dependencies import Database
from ..models.user import *

router = APIRouter(prefix="")

@router.get("/users", response_model=list[UserResponse])
async def get_all(r: Request, database: Database):
    query = select(User) \
        .order_by(User.name.desc())

    users = await database.exec(query)
    return users.all()

@router.get("/users/{id}", response_model=UserResponse)
async def get_one(id: int, r: Request, database: Database):
    user = database.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/user_types", response_model=list[UserTypeResponse])
async def get_all_usertypes(r: Request, database: Database):
    query = select(UserType) \
        .order_by(UserType.id.desc())

    usertypes = await database.exec(query)
    return usertypes.all()

@router.get("/user_types/{id}", response_model=UserTypeResponse)
async def get_one_usertype(id: int, r: Request, database: Database):
    usertype = database.get(UserType, id)
    if not usertype:
        raise HTTPException(status_code=404, detail="Usertype not found")
    return usertype

@router.get("/users/birthdays", response_model=list[UserResponse])
async def get_birthdays(r: Request, database: Database):
    #Implement the birthdays
    pass
