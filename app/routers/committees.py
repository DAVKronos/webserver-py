from typing import Annotated
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import select
from sqlalchemy.orm import selectinload

from ..dependencies import Database
from ..authentication import *
from ..models.committees import *
from ..models.user import *

router = APIRouter(prefix="/committees")


# ============================================================
# GET ALL COMMITTEES
# ============================================================

@router.get("", response_model=list[CommitteeResponse])
async def index(r: Request, database: Database):
    query = (
        select(Committee)
        .order_by(Committee.created_at.desc())
        .options(
            selectinload(Committee.memberships),
            selectinload(Committee.memberships).selectinload(CommitteeMember.user),
        )
    )

    result = await database.exec(query)
    return result.all()


# ============================================================
# GET ONE COMMITTEE
# ============================================================

@router.get("/{id}", response_model=CommitteeResponse)
async def get_committee(id: int, r: Request, database: Database):
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

    return committee


# ============================================================
# CREATE COMMITTEE
# ============================================================

@router.post("", response_model=CommitteeResponse)
async def create_committee(
    data: CommitteeCreate,
    database: Database,
    active_user: Annotated[User, Depends(current_user)]
):
    t = datetime.now(timezone.utc)

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

@router.patch("/{id}", response_model=CommitteeResponse)
async def update_committee(
    id: int,
    data: CommitteeUpdate,
    database: Database,
    active_user: Annotated[User, Depends(current_user)]
):
    committee = await database.get(Committee, id)

    if not committee:
        raise HTTPException(status_code=404, detail="Committee not found")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(committee, key, value)

    committee.updated_at = datetime.now(timezone.utc)

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
    active_user: Annotated[User, Depends(current_user)]
):
    committee = await database.get(Committee, id)

    if not committee:
        raise HTTPException(status_code=404, detail="Committee not found")

    await database.delete(committee)
    await database.commit()
    return


# ============================================================
# GET MEMBERSHIPS
# ============================================================

@router.get("/{id}/memberships", response_model=list[CommitteeMemberResponse])
async def get_memberships(id: int, database: Database):
    query = (
        select(CommitteeMember)
        .where(CommitteeMember.committee_id == id)
        .order_by(CommitteeMember.created_at.desc())
        .options(
            selectinload(CommitteeMember.user),
            selectinload(CommitteeMember.committee)
        )
    )

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
    active_user: Annotated[User, Depends(current_user)]
):
    t = datetime.now(timezone.utc)

    membership = CommitteeMember.model_validate(
        data,
        update={
            "committee_id": id,
            "user_id": active_user.id,
            "created_at": t,
            "updated_at": t
        }
    )

    database.add(membership)
    await database.commit()
    await database.refresh(membership)

    # 🔥 IMPORTANT: re-query with relationships loaded
    result = await database.exec(
        select(CommitteeMember)
        .where(CommitteeMember.id == membership.id)
        .options(
            selectinload(CommitteeMember.user),
            selectinload(CommitteeMember.committee)
        )
    )

    return result.first()


# ============================================================
# DELETE MEMBERSHIP
# ============================================================

@router.delete(
    "/{id}/memberships/{membership_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_membership(
    id: int,
    membership_id: int,
    database: Database,
    active_user: Annotated[User, Depends(current_user)]
):
    membership = await database.get(CommitteeMember, membership_id)

    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")

    if membership.user_id != active_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    await database.delete(membership)
    await database.commit()
    return