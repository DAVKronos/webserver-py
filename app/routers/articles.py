from typing import Annotated, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from sqlmodel import SQLModel, select, func, and_, text
from pydantic import BaseModel, ValidationError
from ..dependencies import Database, ActiveUser
from ..models.article import *
from ..models.comment import *

router = APIRouter(prefix="/newsitems")

@router.get("", response_model=list[ArticlePublicWithCommentCount])
async def index(r: Request, database: Database, active_user: ActiveUser):
    query = select(Article) \
        .where(Article.agreed == True) \
        .limit(None) \
        .offset(None) \
        .order_by(Article.created_at.desc())
    
    articles = await database.exec(query)
    
    # TODO: Make it DRY by using a computed field in the pydantic model?
    from_article = lambda a: ArticlePublicWithCommentCount.model_validate(a, update= {
        'comment_count': len(a.comments)})
    
    return map(from_article, articles.all())

@router.get("/{id}", response_model=ArticlePublicWithCommentCount)
async def get_article(id: int, r: Request, database: Database):
    # TODO filter agreed depending on permission
    query = select(Article) \
        .where(Article.agreed == True) \
        .where(Article.id == id)
    
    article = (await database.exec(query)).first()
    
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    
    from_article = lambda a: ArticlePublicWithCommentCount.model_validate(a, update= {
        'comment_count': len(a.comments)})
    return from_article(article)

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


@router.get("/{id}/comments", response_model=list[CommentPublic])
async def get(id: int, r: Request, database: Database, active_user: ActiveUser):
    # todo: comments are not public!
    query = select(Comment) \
        .where(Article.agreed == True) \
        .limit(None) \
        .offset(None) \
        .order_by(Comment.created_at.desc())
    
    comments = await database.exec(query)
    return comments.all()
