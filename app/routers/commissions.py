from typing import Annotated
from fastapi import APIRouter, Request, Depends, HTTPException
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

@router.get("/{id}", response_model=CommissionResponse)
async def get_one(id: int, r: Request, database: Database):
    commission = await database.get(Commission, id)
    if not commission:
        raise HTTPException(status_code=404, detail="Commission not found")
    return commission

@router.patch("/{id}", response_model=CommissionResponse)
async def update_commission(id: int, data: ComissionUpdate, database: Database, active_user: ActiveUser):
    commission:Commission | None = await database.get(Commission, id)

    if not commission:
        raise HTTPException(status_code=404, detail="Commission not found")
    
    t = datetime.utcnow().date()
    commission.sqlmodel_update(commission, update={'updated_at': t, 'name': data.name, 'name_en': data.name_en, 'description': data.description, 'description_en': data.description_en})

    database.add(commission)
    await database.commit()
    await database.refresh(commission)

    return commission

@router.get("/{id}/commission_memberships",  response_model=list[CommissionMembershipResponse])
async def get_membership(id: int, r: Request, database: Database):
    query = select(CommissionMembership) \
        .where(CommissionMembership.commission_id == id) \
        .order_by(CommissionMembership.created_at.desc())
    
    memberships = await database.exec(query)
    return memberships.all()
