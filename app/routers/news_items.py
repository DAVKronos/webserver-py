from typing import Annotated, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from sqlmodel import SQLModel, select, func, and_, text
from pydantic import BaseModel, ValidationError
from ..dependencies import Database
from ..authentication import *
from ..models.news_item import *
from ..models.user import *
from ..time_utils import now
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/newsitems")

@router.get("", response_model=list[NewsItemResponse])
async def index(r: Request, database: Database):
    query = select(NewsItem) \
        .where(NewsItem.approved == True) \
        .limit(None) \
        .offset(None) \
        .order_by(NewsItem.created_at.desc()) \
        .options(
            selectinload(NewsItem.creator),
            selectinload(NewsItem.comments)
        )
        
    newsitems = await database.exec(query)
    
    return newsitems.all()

@router.get("/{id}", response_model=NewsItemResponse)
async def get_newsitem(id: int, r: Request, database: Database):
    # TODO filter agreed depending on permission
    query = select(NewsItem) \
        .where(NewsItem.approved == True) \
        .where(NewsItem.id == id) \
        .options(
            selectinload(NewsItem.creator),
            selectinload(NewsItem.comments)
        )
    
    newsitem = (await database.exec(query)).first()
    
    if newsitem is None:
        raise HTTPException(status_code=404, detail="NewsItem not found")
    
    return newsitem

@router.post("/", response_model=NewsItemResponse)
async def create_newsitem(data: NewsItemCreate, database: Database, active_user: Annotated[User, Depends(current_user)]):
    t = now()
    try:
        newsitem = NewsItem.model_validate(data, update={'created_at': t, 'updated_at': t, 'user_id': active_user.id })
    except ValidationError as e:
        print(e)
        raise HTTPException(status_code=500, detail="Input data not valid")
    
    database.add(newsitem)
    await database.commit()
    await database.refresh(newsitem)
     
    return NewsItem.model_validate(newsitem, update={"creator":None})
    
@router.patch("/{id}", response_model=NewsItemResponse)
async def update_newsitem(id: int, data: NewsItemUpdate, database: Database):
    newsitem = await database.get(NewsItem, id)
    if not newsitem:
        raise HTTPException(status_code=404, detail="NewsItem not found")
    
    newsitem_dict = data.model_dump(exclude_unset=True)
    newsitem.sqlmodel_update(newsitem_dict, update = {'updated_at': now()})
    database.add(newsitem)
    await database.commit()
    await database.refresh(newsitem)
    return newsitem

@router.delete("/{id}")
async def delete_newsitem(id: int, r: Request, database: Database):
    newsitem: NewsItem | None = await database.get(NewsItem, id)

    if not newsitem:
        raise HTTPException(status_code=404, detail="NewsItem not found")
    await database.delete(newsitem)
    await database.commit()

# TODO: Implement
@router.put("/{id}/photo")
async def insert_photo(r: Request, database: Database):
    pass

# TODO: Implement
@router.put("/{id}/photo")
async def delete_photo(r: Request, database: Database):
    pass

@router.get("/{id}/comments", response_model=list[NewsCommentResponse])
async def get(id: int, database: Database):
    # TODO: comments are not public!
    query = select(NewsComment) \
        .where(
            NewsComment.newsitem_id == id
        ) \
        .order_by(NewsComment.created_at.desc())
    
    comments = await database.exec(query)
    return comments.all()

@router.post("/{id}/comments", response_model=NewsCommentResponse)
async def create_comment(data: NewsCommentCreate, database: Database, active_user: Annotated[User, Depends(current_user)]):
    t = now()
    try:
        comment = NewsComment.model_validate(data, update={'created_at': t, 'updated_at': t, 'user_id': 313 })
        # comment = NewsComment.model_validate(data, update={'created_at': t, 'updated_at': t, 'user_id': active_user.id })
    except ValidationError as error:
        raise HTTPException(status_code=500, detail="Input data not valid")
    database.add(comment)
    await database.commit()
    await database.refresh(comment)

    return comment


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int, database: Database, active_user: Annotated[User, Depends(current_user)]):
    comment:NewsComment | None = await database.get(NewsComment, comment_id)

    if not comment:
        raise HTTPException(status_code=404, detail="NewsComment not found")
    # For now only allow the owner of the comment to remove it
    # TODO: Admins and owner of comment can remove comments
    # if comment.user_id != active_user.id:
    #     raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    await database.delete(comment)
    await database.commit()
    return