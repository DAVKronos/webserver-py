from sqlmodel import select
from typing import Annotated
from fastapi import APIRouter, Request, Depends, HTTPException
from sqlmodel import select

from ..authentication import *

from ..dependencies import Database
from ..models.user import User
from ..models.page import *

router = APIRouter(prefix="/pages")

@router.get("", response_model=list[PageResponse])
async def get_all(r: Request, database: Database):
    query = select(Page) \
        .order_by(Page.pagetag.desc())

    pages = await database.exec(query)
    return pages.all()

@router.get("/{id}", response_model=PageResponse)
async def get(id: int, r: Request, database: Database):
    page = await database.get(Page, id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return page

@router.post("/", response_model=PageResponse)
async def create_page(data: PageCreate, database: Database, active_user: Annotated[User, Depends(current_user)]):
    t = datetime.utcnow()
    try:
        page = Page.model_validate(data, update={'created_at': t, 'updated_at': t, })
    except ValidationError as e:
        # log(e)
        print(e)
        raise HTTPException(status_code=500, detail="Input data not valid")
    
    database.add(page)
    await database.commit()
    await database.refresh(page)
     
    return page

@router.patch("/{id}", response_model=PageResponse)
async def update_page(id: int, data: PageUpdate, database: Database, active_user: Annotated[User, Depends(current_user)]):
    page = await database.get(Page, id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    
    t = datetime.utcnow()
    page_dict = data.model_dump(exclude_unset=True)
    page.sqlmodel_update(page, update = {'updated_at': t, **page_dict})
    database.add(page)

    await database.commit()
    await database.refresh(page)
    return page

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, database: Database, active_user: Annotated[User, Depends(current_user)]):
    page = await database.get(Page, id)

    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    await database.delete(page)
    await database.commit()
    return