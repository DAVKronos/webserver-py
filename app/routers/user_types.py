from fastapi import APIRouter, Request, HTTPException
from sqlmodel import select
from ..dependencies import Database
from ..models.user import *

router = APIRouter(prefix="/user_types")

@router.get("", response_model=list[UserTypeResponse])
async def get_all_usertypes(r: Request, database: Database):
    query = select(UserType) \
        .order_by(UserType.id.desc())

    usertypes = await database.exec(query)
    return usertypes.all()

@router.get("/{id}", response_model=UserTypeResponse)
async def get_one_usertype(id: int, r: Request, database: Database):
    user_type = await database.get(UserType, id)
    if not user_type:
        raise HTTPException(status_code=404, detail="Usertype not found")
    return user_type