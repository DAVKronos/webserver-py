from typing import Annotated
from fastapi import APIRouter, Request, Depends
from ..dependencies import Database
from ..models.commissions import *
from datetime import datetime
router = APIRouter(prefix="/commissions")

@router.get("", response_model=list[CommissionResponse])
async def get_all(r: Request, database: Database):
    query = select(Commission) \
        .order_by(Commission.name.desc())

    commissions = await database.exec(query)
    return commissions.all()

@router.get("/{id}", response_model=CommissionResponse)
async def get_one(id: int, r: Request, database: Database):
    commission = database.get(commission, id)
    if not commission:
        raise HTTPException(status_code=404, detail="Commission not found")
    return commission

@router.get("/{id}/commission_memberships",  response_model=list[CommissionMembershipResponse])
async def get_membership(id: int, r: Request, database: Database):
    query = select(CommissionMembership) \
        .where(CommissionMembership.commission_id == id) \
        .order_by(CommissionMembership.create_at.desc())
    
    memberships = await database.exec(query)
    return memberships.all()
