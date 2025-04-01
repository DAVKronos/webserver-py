from typing import Annotated
from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlmodel import select
from ..dependencies import Database, ActiveUser
from ..models.commission import *
from datetime import datetime

router = APIRouter(prefix="/commissions")

@router.get("", response_model=list[CommissionResponse])
async def get_all(r: Request, database: Database):
    query = select(Commission) \
        .order_by(Commission.name.asc())

    commissions = await database.exec(query)
    return commissions.all()

@router.get("/{commission_id}", response_model=CommissionResponse)
async def get_one(commission_id: int, r: Request, database: Database):
    commission = await database.get(Commission, commission_id)
    if not commission:
        raise HTTPException(status_code=404, detail="Commission not found")
    return commission

@router.get("/{commission_id}/commission_memberships",  response_model=list[CommissionMembershipResponse])
async def get_membership(commission_id: int, r: Request, database: Database):
    query = select(CommissionMembership) \
        .where(CommissionMembership.commission_id == commission_id) \
        .order_by(CommissionMembership.created_at.desc())
    
    memberships = await database.exec(query)
    return memberships.all()

@router.post("/{commission_id}/commission_memberships", response_model=CommissionMembershipResponse)
async def create_membership(commission_id: int, data: CommissionMembershipCreate, database: Database, active_user: ActiveUser):
    t = datetime.utcnow()
    membership = CommissionMembership.model_validate(data, update={'commission_id': commission_id, 'created_at': t, 'updated_at': t})
    database.add(membership)
    await database.commit()
    await database.refresh(membership)

    return membership

@router.delete("/{commission_id}/commission_memberships/{membership_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_membership(commission_id: int, membership_id: int, database: Database, active_user: ActiveUser):
    membership = await database.get(CommissionMembership, membership_id)
    if not membership:
        raise HTTPException(status_code=404, detail="Commission membership not found")
    if membership.user_id != active_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this membership")
    await database.delete(membership)
    await database.commit()

@router.post("", response_model=CommissionResponse)
async def create_commission(data: CommissionCreate, database: Database, active_user: ActiveUser):
    t = datetime.utcnow()
    commission = Commission.model_validate(data, update={'created_at': t, 'updated_at': t})
    database.add(commission)
    await database.commit()
    await database.refresh(commission)

    return commission

@router.patch("/{commission_id}", response_model=CommissionResponse)
async def update_commission(commission_id: int, data: ComissionUpdate, database: Database, active_user: ActiveUser):
    commission = await database.get(Commission, commission_id)

    if not commission:
        raise HTTPException(status_code=404, detail="Commission not found")
    
    t = datetime.utcnow().date()
    commission_data = data.model_dump(exclude_unset=True)
    commission.sqlmodel_update(commission, update={'updated_at': t, **commission_data})

    database.add(commission)
    await database.commit()
    await database.refresh(commission)

    return commission

@router.delete("/{commission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_commission(commission_id: int, database: Database, active_user: ActiveUser):
    commission = await database.get(Commission, commission_id)
    if not commission:
        raise HTTPException(status_code=404, detail="Commission not found")
    await database.delete(commission)
    await database.commit()
