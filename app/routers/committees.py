from typing import Annotated
from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlmodel import select
from ..dependencies import Database
from ..authentication import *
from ..models.committee import *
from ..schemas.committee import *
from datetime import datetime

router = APIRouter(prefix="/committees")

@router.get("", response_model=list[CommitteeResponse])
async def get_all(r: Request, database: Database):
    query = select(Committee) \
        .order_by(Committee.name.asc())

    committees = await database.exec(query)
    return committees.all()

@router.get("/{committee_id}", response_model=CommitteeResponse)
async def get_one(committee_id: int, r: Request, database: Database):
    committee = await database.get(Committee, committee_id)
    if not committee:
        raise HTTPException(status_code=404, detail="Committee not found")
    return committee

@router.get("/{committee_id}/committee_memberships",  response_model=list[CommitteeMemberResponse])
async def get_membership(committee_id: int, r: Request, database: Database):
    query = select(CommitteeMember) \
        .where(CommitteeMember.committee_id == committee_id) \
        .order_by(CommitteeMember.created_at.desc())
    
    memberships = await database.exec(query)
    return memberships.all()

@router.post("/{committee_id}/committee_memberships", response_model=CommitteeMemberResponse)
async def create_membership(committee_id: int, data: CommitteeMemberCreate, database: Database, active_user: Annotated[User, Depends(current_user)]):
    t = datetime.utcnow()
    membership = CommitteeMember.model_validate(data, update={'committee_id': committee_id, 'created_at': t, 'updated_at': t})
    database.add(membership)
    await database.commit()
    await database.refresh(membership)

    return membership

@router.delete("/{committee_id}/committee_memberships/{membership_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_membership(committee_id: int, membership_id: int, database: Database, active_user: Annotated[User, Depends(current_user)]):
    membership = await database.get(CommitteeMember, membership_id)
    if not membership:
        raise HTTPException(status_code=404, detail="Committee membership not found")
    if membership.user_id != active_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this membership")
    await database.delete(membership)
    await database.commit()

@router.post("", response_model=CommitteeResponse)
async def create_committee(data: CommitteeCreate, database: Database, active_user: Annotated[User, Depends(current_user)]):
    t = datetime.utcnow()
    committee = Committee.model_validate(data, update={'created_at': t, 'updated_at': t})
    database.add(committee)
    await database.commit()
    await database.refresh(committee)

    return committee

@router.patch("/{committee_id}", response_model=CommitteeResponse)
async def update_committee(committee_id: int, data: CommitteeCreate, database: Database, active_user: Annotated[User, Depends(current_user)]):
    committee = await database.get(Committee, committee_id)

    if not committee:
        raise HTTPException(status_code=404, detail="Committee not found")
    
    t = datetime.utcnow().date()
    committee_data = data.model_dump(exclude_unset=True)
    committee.sqlmodel_update(committee, update={'updated_at': t, **committee_data})

    database.add(committee)
    await database.commit()
    await database.refresh(committee)

    return committee

@router.delete("/{committee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_committee(committee_id: int, database: Database, active_user: Annotated[User, Depends(current_user)]):
    committee = await database.get(Committee, committee_id)
    if not committee:
        raise HTTPException(status_code=404, detail="Committee not found")
    await database.delete(committee)
    await database.commit()
