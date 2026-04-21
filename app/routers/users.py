from fastapi import APIRouter, Request, HTTPException, Depends, status
from sqlalchemy.sql import extract
from sqlmodel import select, or_
from ..dependencies import Database
from datetime import date
from ..models.user import *
from ..models.committees import *
from typing import Annotated
from ..authentication import get_current_user
from ..time_utils import now
from ..permissions import *

# All user endpoints need authentication
router = APIRouter(
    prefix="/users",
    dependencies=[Depends(get_current_user)]
)

@router.get("")
async def get_all(database: Database, user_context: Annotated[UserContext, Depends(get_current_user)]):
    query = select(User) \
        .order_by(User.name.asc())
    users = (await database.exec(query)).all()

    users_response = []
    for user in users:
        if user_can(user_context.permissions, VIEW_EXTENDED, "User", user):
            users_response.append(UserExtendedResponse.model_validate(user))
        else:
            users_response.append(UserBasicResponse.model_validate(user))

    return users_response

@router.get("/birthdays", response_model=list[UserBasicResponse])
async def get_birthdays(database: Database):
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

@router.get("/{id}")
async def get_one(id: int, database: Database, user_context: Annotated[UserContext, Depends(get_current_user)]):
    user = await database.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_can(user_context.permissions, VIEW_EXTENDED, "User", user):
        return UserExtendedResponse.model_validate(user)
    
    return UserBasicResponse.model_validate(user)


@router.delete("/{id}")
async def delete_user(id: int, database: Database, user_context: Annotated[UserContext, Depends(get_current_user)]):
    user = await database.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user_can(user_context.permissions, DELETE, "User", user):
        raise HTTPException(status.HTTP_403_FORBIDDEN)
    
    await database.delete(user)
    await database.commit()

@router.patch("/{id}", response_model=UserExtendedResponse)
async def update_user(id: int, data: UserUpdate, database: Database, user_context: Annotated[UserContext, Depends(get_current_user)]):
    user = await database.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user_can(user_context.permissions, EDIT, "User", user):
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    user_dict = data.model_dump(exclude_unset=True)
    user.sqlmodel_update(user_dict, update = {'updated_at': now()})
    database.add(user)
    await database.commit()
    await database.refresh(user)
    return user

@router.get("/{id}/committees", response_model=list[CommitteePublicResponse])
async def get_committees(id: int, database: Database):
    query = (
        select(Committee)
        .join(CommitteeMember)
        .where(CommitteeMember.user_id == id)
    )
    
    results = await database.exec(query)
    return results.all()