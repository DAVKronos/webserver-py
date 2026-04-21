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

router = APIRouter(prefix="/committees")


# ============================================================
# GET ALL COMMITTEES
# ============================================================

@router.get("")
async def index(r: Request, database: Database, user_context: Annotated[Optional[UserContext], Depends(get_optional_user)]):
    query = (
        select(Committee) \
        .order_by(Committee.created_at.desc())
    )
    committees = (await database.exec(query)).all()

    if not user or not user_can(user_context.permissions, VIEW, "Subscription", committees):
        return [CommitteePublicResponse.model_validate(committee) for committee in committees]
    return [CommitteeExtendedResponse.model_validate(committee) for committee in committees]

# ============================================================
# GET ONE COMMITTEE
# ============================================================

@router.get("/{id}")
async def get_committee(id: int, r: Request, database: Database, user_context: Annotated[Optional[UserContext], Depends(get_optional_user)]):
    query = (
        select(Committee)
        .where(Committee.id == id)
        .options(
            selectinload(Committee.memberships),
            selectinload(Committee.memberships).selectinload(CommitteeMember.user),
        )
    )
    committee = (await database.exec(query)).first()

    if committee is None:
        raise HTTPException(status_code=404, detail="Committee not found")
    
    if not user_context or not user_can(user_context.permissions, VIEW, "Subscription", committee):
        return CommitteePublicResponse.model_validate(committee)
    return CommitteeExtendedResponse.model_validate(committee)

# ============================================================
# CREATE COMMITTEE
# ============================================================

@router.post("", response_model=CommitteeExtendedResponse)
async def create_committee(
    data: CommitteeCreate,
    database: Database,
    user_context: Annotated[UserContext, Depends(get_current_user)]
):
    if not user_can(user_context.permissions, CREATE, "Committee"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    t = now()
    committee = Committee.model_validate(
        data,
        update={
            "created_at": t,
            "updated_at": t
        }
    )

    database.add(committee)
    await database.commit()
    await database.refresh(committee)

    return committee


# ============================================================
# UPDATE COMMITTEE
# ============================================================

@router.patch("/{id}", response_model=CommitteeExtendedResponse)
async def update_committee(
    id: int,
    data: CommitteeUpdate,
    database: Database,
    user_context: Annotated[UserContext, Depends(get_current_user)]
):
    committee = await database.get(Committee, id)

    if not committee:
        raise HTTPException(status_code=404, detail="Committee not found")
    if not user_can(user_context.permissions, EDIT, "Committee", committee):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    update_data = data.model_dump(exclude_unset=True)
    committee.sqlmodel_update(update_data, update = {'updated_at': now()})

    database.add(committee)
    await database.commit()
    await database.refresh(committee)

    return committee


# ============================================================
# DELETE COMMITTEE
# ============================================================

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_committee(
    id: int,
    database: Database,
    user_context: Annotated[UserContext, Depends(get_current_user)]
):
    committee = await database.get(Committee, id)

    if not committee:
        raise HTTPException(status_code=404, detail="Committee not found")
    if not user_can(user_context.permissions, DELETE, "Committee", committee):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    await database.delete(committee)
    await database.commit()
    return


# ============================================================
# GET MEMBERSHIPS
# ============================================================

@router.get("/{id}/memberships", response_model=list[CommitteeMemberResponse])
async def get_memberships(id: int, database: Database, user_context: Annotated[UserContext, Depends(get_current_user)]):
    query = (
        select(CommitteeMember) \
        .where(CommitteeMember.committee_id == id) \
        .order_by(CommitteeMember.created_at.desc()) 
    )
    if not user_can(user_context.permissions, VIEW, "CommitteeMember"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    result = await database.exec(query)
    return result.all()


# ============================================================
# CREATE MEMBERSHIP
# ============================================================

@router.post("/{id}/memberships", response_model=CommitteeMemberResponse)
async def create_membership(
    id: int,
    data: CommitteeMemberCreate,
    database: Database,
    user_context: Annotated[UserContext, Depends(get_current_user)]
):
    if not user_can(user_context.permissions, CREATE, "CommitteeMember"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    t = now()

    membership = CommitteeMember.model_validate(
        data,
        update={
            "committee_id": id,
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
    membership = await database.get(CommitteeMember, membership_id)

    if not membership:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Membership not found")
    
    if not user_can(user_context.permissions, DELETE, "CommitteeMember", membership):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
    await database.delete(membership)
    await database.commit()
    return