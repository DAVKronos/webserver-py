from typing import Annotated
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import select
from sqlalchemy.orm import selectinload

from ..dependencies import Database
from ..authentication import *
from ..models.committees import *
from ..models.user import *
from ..time_utils import now
from ..permissions import *

router = APIRouter(prefix="/mailinglists")

from ..models.mailinglists import MailingList, MailingListResponse, MailingListCreate, MailingListUpdate
from ..models.mailinglists import MailingListMemberCreate, MailingListMemberResponse, MailingListMember

# ============================================================
# GET ALL LISTS
# ============================================================

@router.get("")
async def get_lists(database: Database, user_context: Annotated[UserContext, Depends(get_current_user)]):
    if not user_can(user_context.permissions, VIEW, "MailingList"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    query = (
        select(MailingList)
    )
    lists = (await database.exec(query)).all()
    return [MailingListResponse.model_validate(ls) for ls in lists]

# ============================================================
# GET ONE LIST
# ============================================================

@router.get("/{id}")
async def get_list(id: int, database: Database, user_context: Annotated[Optional[UserContext], Depends(get_optional_user)]):
    if not user_can(user_context.permissions, VIEW, "MailingList"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    query = (
        select(MailingList) \
        .where(MailingList.id == id)
    )
    mlist = (await database.exec(query)).first()
    if not list:
        raise HTTPException(status_code=404, detail="Mailing list not found")

    return MailingListResponse.model_validate(mlist)

# ============================================================
# CREATE LIST
# ============================================================

@router.post("", response_model=MailingListResponse)
async def create_list(
    data: MailingListCreate,
    database: Database,
    user_context: Annotated[UserContext, Depends(get_current_user)]
):
    if not user_can(user_context.permissions, CREATE, "MailingList"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    t = now()
    mlist = MailingList.model_validate(
        data,
        update={
            "created_at": t,
            "updated_at": t
        }
    )

    database.add(mlist)
    await database.commit()
    await database.refresh(mlist)

    return mlist


# ============================================================
# UPDATE LIST
# ============================================================

@router.patch("/{id}", response_model=MailingListResponse)
async def update_committee(
    id: int,
    data: MailingListUpdate,
    database: Database,
    user_context: Annotated[UserContext, Depends(get_current_user)]
):
    mlist = await database.get(MailingList, id)

    if not mlist:
        raise HTTPException(status_code=404, detail="Mailing list not found")
    if not user_can(user_context.permissions, EDIT, "MailingList", mlist):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    update_data = data.model_dump(exclude_unset=True)
    mlist.sqlmodel_update(update_data, update = {'updated_at': now()})

    database.add(mlist)
    await database.commit()
    await database.refresh(mlist)

    return mlist


# ============================================================
# DELETE LIST
# ============================================================

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_list(
    id: int,
    database: Database,
    user_context: Annotated[UserContext, Depends(get_current_user)]
):
    mlist = await database.get(MailingList, id)

    if not mlist:
        raise HTTPException(status_code=404, detail="Mailing list not found")
    if not user_can(user_context.permissions, DELETE, "MailingList", mlist):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    await database.delete(mlist)
    await database.commit()
    return


# ============================================================
# CREATE MEMBERSHIP
# ============================================================

@router.post("/{id}/members", response_model=MailingListMemberResponse)
async def create_membership(
    id: int,
    data: MailingListMemberCreate,
    database: Database,
    user_context: Annotated[UserContext, Depends(get_current_user)]
):
    if not user_can(user_context.permissions, CREATE, "MailingList"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    t = now()

    membership = MailingListMember.model_validate(
        data,
        update={
            "mailing_list_id": id,
            "created_at": t,
            "updated_at": t
        }
    )

    database.add(membership)
    await database.commit()
    await database.refresh(membership)
    return membership

# ============================================================
# DELETE MEMBERSHIP
# ============================================================

@router.delete("/{id}/memberships/{membership_id}")
async def delete_membership(
    id: int,
    membership_id: int,
    database: Database,
    user_context: Annotated[UserContext, Depends(get_current_user)]
):
    membership = await database.get(MailingListMember, membership_id)

    if not membership:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Membership not found")
    
    if not user_can(user_context.permissions, DELETE, "MailingList", membership):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    await database.delete(membership)
    await database.commit()
    return