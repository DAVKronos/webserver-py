from datetime import datetime, timezone
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from pydantic import BaseModel, ValidationError
from sqlmodel import SQLModel, and_, func, select, text

from ..authentication import *
from ..dependencies import Database
from ..models.article import *
from ..models.comment import CommentCreate, CommentPublic, CommentUpdate

router = APIRouter(prefix="/newsitems")

@router.get("", response_model=list[ArticlePublicWithCommentCount])
async def index(r: Request, database: Database):
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

@router.get("/agree", response_model=list[ArticlePublic])
async def get_to_be_agreed(r: Request, database: Database):
    #TODO: Add permission check

    query = select(Article) \
        .where(Article.agreed == False) \
    
    articles = await database.exec(query)
    
    return articles.all()

@router.get("/{id}", response_model=ArticlePublicWithCommentCount)
async def get_article(id: int, r: Request, database: Database):
    # TODO filter agreed depending on permission
    query = select(Article) \
        .where(Article.id == id)
        # .where(Article.agreed == True) \
    
    article = (await database.exec(query)).first()
    
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    
    from_article = lambda a: ArticlePublicWithCommentCount.model_validate(a, update= {
        'comment_count': len(a.comments)})
    return from_article(article)

@router.get("/{id}/agree", response_model=ArticlePublic)
async def agree_article(id: int, r: Request, database: Database):
    article = await database.get(Article, id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    t = datetime.utcnow()
    article.sqlmodel_update(article, update = {'updated_at': t, 'agreed': True})
    database.add(article)

    await database.commit()
    await database.refresh(article)
    return article

@router.post("/", response_model=ArticlePublic)
async def create_article(data: ArticleCreate, database: Database, active_user: Annotated[User, Depends(current_user)]):
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
async def update_article(id: int, data: ArticleUpdate, database: Database, active_user: Annotated[User, Depends(current_user)]):
    article = await database.get(Article, id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    t = datetime.utcnow()
    article_dict = data.model_dump(exclude_unset=True)
    article.sqlmodel_update(article, update = {'updated_at': t, **article_dict})
    database.add(article)

    await database.commit()
    await database.refresh(article)
    return article


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, database: Database):
    article = await database.get(Article, id)

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    await database.delete(article)
    await database.commit()
    return

@router.put("/{id}/photo")
async def insert_photo(r: Request, database: Database):
    pass

@router.put("/{id}/photo")
async def delete_photo(r: Request, database: Database):
    pass

@router.get("/{id}/comments", response_model=list[CommentPublic])
async def get(id: int, database: Database):
    # todo: comments are not public!
    query = select(Comment) \
        .where(
            Comment.commentable_id == id,
            # Article.agreed == True
        ).limit(None) \
        .offset(None) \
        .order_by(Comment.created_at.desc())
    
    comments = await database.exec(query)
    return comments.all()

@router.post("/{id}/comments", response_model=CommentPublic)
async def create_comment(data: CommentCreate, database: Database, active_user: Annotated[User, Depends(current_user)]):
    t = datetime.utcnow()
    try:
        comment = Comment.model_validate(data, update={'created_at': t, 'updated_at': t, 'user_id': active_user.id })
    except ValidationError as error:
        raise HTTPException(status_code=500, detail="Input data not valid")
    database.add(comment)
    await database.commit()
    await database.refresh(comment)

    return comment

@router.patch("/{article_id}/comments/{comment_id}", response_model=CommentPublic)
async def update_comment( comment_id: int, data: CommentUpdate, database: Database, active_user: Annotated[User, Depends(current_user)]):
    comment:Comment | None = await database.get(Comment, comment_id)
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    #For now only allow the owner of the comment to remove it
    if comment.user_id != active_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this comment")
    t = datetime.utcnow()
    comment.sqlmodel_update(comment, update={'updated_at': t, 'commenttext': data.commenttext})

    database.add(comment)
    await database.commit()
    await database.refresh(comment)

    return comment

@router.delete("/{article_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int, database: Database, active_user: Annotated[User, Depends(current_user)]):
    comment:Comment | None = await database.get(Comment, comment_id)

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    #For now only allow the owner of the comment to remove it
    if comment.user_id != active_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    await database.delete(comment)
    await database.commit()
    return

