from typing import Annotated
import datetime
from fastapi import APIRouter, Request, Depends, Query, HTTPException, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import column, func
from sqlmodel import select
from ..dependencies import Database
from ..authentication import *
from ..models.agendaitem import *
from ..time_utils import now
from ..permissions import *

router = APIRouter()

@router.get("/agendaitems")
async def get(
    r: Request, 
    database: Database, 
    user: Annotated[Optional[User], Depends(get_optional_user)],
    year: Annotated[int, Query(alias="date[year]")] = datetime.now().year,
    month: Annotated[int, Query(alias="date[month]")] = datetime.now().month,
):
    query = select(AgendaItem) \
        .order_by(AgendaItem.date.asc()) \
        .where(func.extract("year", AgendaItem.date) == year) \
        .where(func.extract("month", AgendaItem.date) == month)
    agendaitems = (await database.exec(query)).all()
    
    if user: # Private Response
        return [AgendaItemExtendedResponse.model_validate(item) for item in agendaitems]
    
    # Public response
    return [AgendaItemPublicResponse.model_validate(item) for item in agendaitems if not item.is_internal]


@router.get("/agendaitems/{id}")
async def get(id : int , r: Request, database: Database, user: Annotated[Optional[User], Depends(get_optional_user)]):
    agendaitem = await database.get(AgendaItem, id) 
    if agendaitem is None : 
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Agenda item not found")
    
    if user:
        return AgendaItemExtendedResponse.model_validate(agendaitem)
    
    if agendaitem.is_internal:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="You must login to view this agenda item.")
    
    return AgendaItemPublicResponse.model_validate(agendaitem)

@router.get("/agendaitemtypes/{id}", response_model=AgendaItemTypeResponse)
async def get(id : int, r: Request, database: Database):
    agendaitemType = await database.get(AgendaItemType, id) 
    if agendaitemType is None : 
        raise HTTPException(status_code=404, detail="Agenda item type not found")
    return agendaitemType

@router.get("/agendaitemtypes", response_model=list[AgendaItemType])
async def get(r: Request, database: Database):
    query = select(AgendaItemType)
    agendaitemTypes = await database.exec(query) 
    if agendaitemTypes is None : 
        raise HTTPException(status_code=404, detail="Agenda item type not found")
    return agendaitemTypes.all()



@router.get("/agendaitems/{id}/subscriptions", response_model=list[SubscriptionResponse])
async def get(r: Request, id: int, database: Database, user: Annotated[User, Depends(get_current_user)]
):
    query = select(Subscription) \
        .where(Subscription.agendaitem_id == id) \
        .order_by(Subscription.created_at.asc()) \
        
    subscriptions = await database.exec(query)       
    
    return subscriptions



@router.post("/agendaitems", response_model=AgendaItemExtendedResponse)
async def create_agenda_item(data: AgendaItemCreate, database: Database, user: Annotated[User, Depends(get_current_user)]):
    if not user_can(user, CREATE, "AgendaItem"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions.")
    
    t = now()
    agenda_item = AgendaItem.model_validate(data, update={'created_at': t, 'updated_at': t, 'created_by_user_id': user.id})

    database.add(agenda_item)
    await database.commit()
    await database.refresh(agenda_item)
     
    return agenda_item



@router.delete("/agendaitems/{id}")
async def delete_agendaitem(id: int, database: Database, user: Annotated[User, Depends(get_current_user)]):
    if not user_can(user, DELETE, "AgendaItem"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions.")
    
    agendaitem: AgendaItem | None = await database.get(AgendaItem, id)

    if not agendaitem:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="AgendaItem not found")

    await database.delete(agendaitem)
    await database.commit()
    return


@router.patch("/agendaitems/{id}", response_model=AgendaItemExtendedResponse)
async def update_agendaitem( id: int, data: AgendaItemUpdate, database: Database, user: Annotated[User, Depends(get_current_user)]):
    if not user_can(user, EDIT, "AgendaItem"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions.")
    
    agendaitem: AgendaItem | None = await database.get(AgendaItem, id)
    
    if not agendaitem:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="AgendaItem not found")
    t = now()
    agendaitem_data = data.model_dump(exclude_unset=True)
    agendaitem.sqlmodel_update(agendaitem, update={'updated_at': t, **agendaitem_data})

    database.add(agendaitem)
    await database.commit()
    await database.refresh(agendaitem)

    return agendaitem
