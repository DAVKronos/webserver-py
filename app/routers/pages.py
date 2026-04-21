from sqlmodel import select
from typing import Annotated
from fastapi import APIRouter, Request, HTTPException, status, Depends
from sqlmodel import select
from ..dependencies import Database
from ..models.page import *
from ..permissions import *
from ..authentication import get_current_user, get_optional_user
from ..time_utils import now

router = APIRouter(prefix="/pages")

@router.get("", response_model=list[PageResponse])
async def get_all(database: Database, user_context: Annotated[Optional[UserContext], Depends(get_optional_user)]):
    query = select(Page)

    pages: List[Page] = (await database.exec(query)).all()
    if not user_context: # Not logged in
        pages = filter(lambda page: page.is_public, pages)

    return pages

@router.get("/{id}", response_model=PageResponse)
async def get(id: int, database: Database, user_context: Annotated[Optional[UserContext], Depends(get_optional_user)]):
    page = await database.get(Page, id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    if not user_context and not page.is_public:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions.")
    return page

@router.post("", response_model=PageResponse)
async def create_page(
    data: PageCreate,
    database: Database,
    user_context: Annotated[UserContext, Depends(get_current_user)]
):
    if not user_can(user_context.permissions, CREATE, "Page"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    t = now()
    page = Page.model_validate(data, update={"created_at": t, "updated_at": t})

    database.add(page)
    await database.commit()
    await database.refresh(page)

    return page

@router.patch("/{id}", response_model=PageResponse)
async def update_page(
    id: int,
    data: PageUpdate,
    database: Database,
    user_context: Annotated[UserContext, Depends(get_current_user)]
):
    page = await database.get(Page, id)

    if not page:
        raise HTTPException(status_code=404, detail="Committee not found")
    if not user_can(user_context.permissions, EDIT, "Page", page):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    update_data = data.model_dump(exclude_unset=True)
    page.sqlmodel_update(update_data, update = {'updated_at': now()})

    database.add(page)
    await database.commit()
    await database.refresh(page)

    return page

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_page(
    id: int,
    database: Database,
    user_context: Annotated[UserContext, Depends(get_current_user)]
):
    committee = await database.get(Page, id)

    if not committee:
        raise HTTPException(status_code=404, detail="Committee not found")
    if not user_can(user_context.permissions, DELETE, "Committee", committee):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    await database.delete(committee)
    await database.commit()
    return 