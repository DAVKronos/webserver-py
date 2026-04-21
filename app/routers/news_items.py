from typing import Annotated, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import select
from pydantic import  ValidationError
from ..dependencies import Database
from ..authentication import *
from ..models.news_item import *
from ..models.user import *
from ..time_utils import now
from ..permissions import *

router = APIRouter(prefix="/newsitems")

@router.get("")
async def index(database: Database, user_context: Annotated[Optional[UserContext], Depends(get_optional_user)]):
    query = select(NewsItem) \
        .where(NewsItem.approved == True) \
        .order_by(NewsItem.created_at.desc())
    newsitems = (await database.exec(query)).all()

    if not user_context or not user_can(user_context.permissions, VIEW_EXTENDED, "NewsItem"):
        return [NewsItemPublicResponse.model_validate(item) for item in newsitems]
    return [NewsItemExtendedResponse.model_validate(item) for item in newsitems]

@router.get("/{id}")
async def get_newsitem(id: int, database: Database, user_context: Annotated[Optional[UserContext], Depends(get_optional_user)]):
    query = select(NewsItem) \
        .where(NewsItem.approved == True) \
        .where(NewsItem.id == id)
    
    newsitem = (await database.exec(query)).first()    
    if newsitem is None:
        raise HTTPException(status_code=404, detail="NewsItem not found")
    
    if not user_context or not user_can(user_context.permissions, VIEW_EXTENDED, "NewsItem"):
        return NewsItemPublicResponse.model_validate(newsitem)
    return NewsItemExtendedResponse.model_validate(newsitem)

@router.post("/", response_model=NewsItemExtendedResponse)
async def create_newsitem(data: NewsItemCreate, database: Database, user_context: Annotated[UserContext, Depends(get_current_user)]):
    if not user_can(user_context.permissions, CREATE, "NewsItem"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions.")
    
    t = now()
    newsitem = NewsItem.model_validate(data, update={'created_at': t, 'updated_at': t, 'user_id': user_context.user.id })
    
    database.add(newsitem)
    await database.commit()
    await database.refresh(newsitem)
     
    return newsitem

@router.patch("/{id}", response_model=NewsItemExtendedResponse)
async def update_newsitem(id: int, data: NewsItemUpdate, database: Database, user_context: Annotated[UserContext, Depends(get_current_user)]):

    newsitem = await database.get(NewsItem, id)
    if not newsitem:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="NewsItem not found")
    if not user_can(user_context.permissions, EDIT, "NewsItem", newsitem):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions.")
    
    newsitem_dict = data.model_dump(exclude_unset=True)
    newsitem.sqlmodel_update(newsitem_dict, update = {'updated_at': now()})
    database.add(newsitem)
    await database.commit()
    await database.refresh(newsitem)
    return newsitem

@router.delete("/{id}")
async def delete_newsitem(id: int, database: Database, user_context: Annotated[UserContext, Depends(get_current_user)]):
    newsitem = await database.get(NewsItem, id)

    if not newsitem:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="NewsItem not found")
    if not user_can(user_context.permissions, CREATE, "NewsItem", newsitem):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions.")
    await database.delete(newsitem)
    await database.commit()

# TODO: Implement
@router.put("/{id}/photo")
async def insert_photo(database: Database):
    pass

# TODO: Implement
@router.put("/{id}/photo")
async def delete_photo(database: Database):
    pass

@router.get("/{id}/comments", response_model=list[NewsCommentResponse])
async def get(id: int, database: Database, user_context: Annotated[UserContext, Depends(get_current_user)]):
    if not user_can(user_context.permissions, VIEW, "Comment"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions.")
    
    query = select(NewsComment) \
        .where(
            NewsComment.newsitem_id == id
        ) \
        .order_by(NewsComment.created_at.desc())
    
    comments = await database.exec(query)
    return comments.all()

@router.post("/{id}/comments", response_model=NewsCommentResponse)
async def create_comment(data: NewsCommentCreate, database: Database, user_context: Annotated[UserContext, Depends(get_current_user)]):
    if not user_can(user_context.permissions, CREATE, "Comment"):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions.")
    
    t = now()
    comment = NewsComment.model_validate(data, update={'created_at': t, 'updated_at': t, 'user_id': user.id })
    database.add(comment)
    await database.commit()
    await database.refresh(comment)

    return comment


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int, database: Database, user_context: Annotated[UserContext, Depends(get_current_user)]):
    comment:NewsComment | None = await database.get(NewsComment, comment_id)

    if not comment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="NewsComment not found")
    if not user_can(user_context.permissions, DELETE, "Comment", comment):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not enough permissions.")
    
    await database.delete(comment)
    await database.commit()
    return