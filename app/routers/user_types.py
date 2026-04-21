from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import select
from ..dependencies import Database
from ..models.user import *
from ..authentication import get_current_user
from ..permissions import UserContext

router = APIRouter(prefix="/user_type")

@router.get("s", response_model=list[UserTypeResponse])
async def index(database: Database, user_context: Annotated[UserContext, Depends(get_current_user)]):
    if not user_context:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    
    query = select(UserType) \
        .order_by(UserType.id.desc())
        
    usertypes = await database.exec(query)
    
    return usertypes.all()

@router.get("/{id}", response_model=UserTypeResponse)
async def get_usertype(id: int, database: Database, user_context: Annotated[UserContext, Depends(get_current_user)]):
    if not user_context:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    
    query = select(UserType) \
        .where(UserType.id == id)
    
    user_type = (await database.exec(query)).first()
    
    if user_type is None:
        raise HTTPException(status_code=404, detail="Usertype not found")
    
    return user_type