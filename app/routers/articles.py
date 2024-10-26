from typing import Annotated, Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from ..dependencies import Database, ActiveUser
from ..queries import articles
from ..models.article import *
from sqlmodel import SQLModel, select, func, and_, text
from pydantic import BaseModel, ValidationError
from datetime import datetime, timezone

router = APIRouter(prefix="/newsitems")

#@router.get("", response_model = list[ArticlePublicWithCommentCount])
@router.get("", response_model=list[ArticlePublicWithCommentCount])
async def get(r: Request, database: Database, active_user: ActiveUser):
    res = await articles.get(database)
    return [a for a in res if a.agreed]

@router.get("/{id}", response_model=ArticlePublicWithCommentCount)
async def get_by_id(id: int, r: Request, database: Database):
    result = await articles.get(database, id)
    
    if len(result) == 0:
        raise HTTPException(status_code=404, detail="Article not found")
    # TODO filter agreed depending on permission
    return result[0]

@router.post("/", response_model=ArticlePublic)
async def create_article(data: ArticleCreate, database: Database, active_user: ActiveUser):
    t = datetime.utcnow()
    try:
        article = Article.model_validate(data, update={'created_at': t, 'updated_at': t, 'agreed': False, 'user_id': active_user.id })
    except ValidationError as e:
        # log(e)
        print(e)
        raise HTTPException(status_code=500, detail="Input data not valid")
    
    database.add(article)
    await database.commit()
    await database.refresh(article)
     
    return ArticlePublic.model_validate(article, update={"user":None})
    return article
    
@router.patch("/{id}", response_model=ArticlePublic)
async def update_article(data: ArticleUpdate, database: Database, active_user: ActiveUser):
    article = database.get(Article, id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    article_dict = data.model_dump(exclude_unset=True)
    article.sqlmodel_update(article_dict, update = {updated_at: datetime.now(timezone.utc)})
    database.add(article)
    database.commit()
    database.refresh(article)
    return article

@router.delete("/{id}")
async def delete(r: Request, database: Database):
    pass

@router.put("/{id}/photo")
async def insert_photo(r: Request, database: Database):
    pass

@router.put("/{id}/photo")
async def delete_photo(r: Request, database: Database):
    pass


@router.get("/{id}/comments", response_class=JSONResponse)
async def get(id: int, r: Request, database: Database, active_user: ActiveUser):
    res = await articles.get_comments(database, id)
    # todo: comments are not public!
    # return res
