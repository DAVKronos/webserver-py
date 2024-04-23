from typing import Annotated
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from ..dependencies import DepDatabase
from ..queries import users
from ..models.user import *
from ..models.authentication import get_active_user


router = APIRouter(prefix="")


@router.get("/users", response_class=JSONResponse)
async def get(r: Request, database: DepDatabase):
    res = await users.get(database)
    return res
    
@router.get("/users/{id}", response_class=JSONResponse)
async def get(id: int, r: Request, database: DepDatabase):
    res = await users.get(database, id)
    return res

@router.get("/user_types", response_class=JSONResponse)
async def usertypes(r: Request, database: DepDatabase):
    res = await users.get_usertypes(database)
    return res

@router.get("/user_types/{id}",  response_class=JSONResponse)
async def usertypes(id: int, r: Request, database: DepDatabase):
    res = await users.get_usertypes(database, id)
    return res

@router.get("/users/birthdays",  response_class=JSONResponse)
async def birthdays(r: Request, database: DepDatabase):
    pass
    
