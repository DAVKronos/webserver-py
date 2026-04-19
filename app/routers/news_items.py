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

router = APIRouter(prefix="/newsitems")

@router.get("")
async def index(r: Request, database: Database, user: Annotated[Optional[User], Depends(get_optional_user)]):
    query = select(NewsItem) \
        .where(NewsItem.approved == True) \
        .order_by(NewsItem.created_at.desc())
    newsitems = (await database.exec(query)).all()

    if user:
        return [NewsItemPrivateResponse.model_validate(item) for item in newsitems]
    return [NewsItemPublicResponse.model_validate(item) for item in newsitems]

@router.get("/{id}")
async def get_newsitem(id: int, r: Request, database: Database, user: Annotated[Optional[User], Depends(get_optional_user)]):
    query = select(NewsItem) \
        .where(NewsItem.approved == True) \
        .where(NewsItem.id == id)
    
    newsitem = (await database.exec(query)).first()    
    if newsitem is None:
        raise HTTPException(status_code=404, detail="NewsItem not found")
    
    if user:
        return NewsItemPrivateResponse.model_validate(newsitem)
    return NewsItemPublicResponse.model_validate(newsitem)

@router.post("/", response_model=NewsItemPrivateResponse)
async def create_newsitem(data: NewsItemCreate, database: Database, user: Annotated[User, Depends(get_current_user)]):
    t = now()
    try:
        newsitem = NewsItem.model_validate(data, update={'created_at': t, 'updated_at': t, 'user_id': user.id })
    except ValidationError as e:
        print(e)
        raise HTTPException(status_code=500, detail="Input data not valid")
    
    database.add(newsitem)
    await database.commit()
    await database.refresh(newsitem)
     
    return newsitem
    
@router.patch("/{id}", response_model=NewsItemPrivateResponse)
async def update_newsitem(id: int, data: NewsItemUpdate, database: Database, user: Annotated[User, Depends(get_current_user)]):
    newsitem = await database.get(NewsItem, id)
    if not newsitem:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="NewsItem not found")
    
    # TODO: admins can patch as well
    if newsitem.creator_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    newsitem_dict = data.model_dump(exclude_unset=True)
    newsitem.sqlmodel_update(newsitem_dict, update = {'updated_at': now()})
    database.add(newsitem)
    await database.commit()
    await database.refresh(newsitem)
    return newsitem

@router.delete("/{id}")
async def delete_newsitem(id: int, r: Request, database: Database, user: Annotated[User, Depends(get_current_user)]):
    newsitem = await database.get(NewsItem, id)

    if not newsitem:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="NewsItem not found")
    if newsitem.creator_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not authorized")
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
async def get(id: int, database: Database, user: Annotated[User, Depends(get_current_user)]):
    query = select(NewsComment) \
        .where(
            NewsComment.newsitem_id == id
        ) \
        .order_by(NewsComment.created_at.desc())
    
    comments = await database.exec(query)
    return comments.all()

@router.post("/{id}/comments", response_model=NewsCommentResponse)
async def create_comment(data: NewsCommentCreate, database: Database, user: Annotated[User, Depends(get_current_user)]):
    t = now()
    try:
        comment = NewsComment.model_validate(data, update={'created_at': t, 'updated_at': t, 'user_id': user.id })
    except ValidationError:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Input data not valid")
    database.add(comment)
    await database.commit()
    await database.refresh(comment)

    return comment


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int, database: Database, user: Annotated[User, Depends(get_current_user)]):
    comment:NewsComment | None = await database.get(NewsComment, comment_id)

    if not comment:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="NewsComment not found")
    # TODO: Admins can remove comments
    if comment.user_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this comment")
    await database.delete(comment)
    await database.commit()
    return