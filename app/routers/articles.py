from typing import Annotated
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from ..dependencies import DepDatabase
from ..queries import articles

from sqlmodel import select, func, and_, text

from app import dependencies as deps
from app.models import Article, ArticlePublic, ArticlePublicWithCommentCount, Comment, User, UserPublic
router = APIRouter(prefix="/newsitems")

@router.get("", response_model = list[ArticlePublicWithCommentCount])
async def get(database: deps.Database):
    return (await articles.get(database))
    

@router.get("/{id}", response_model=ArticlePublicWithCommentCount)
async def get(id: int, r: Request, database: deps.Database):
    result = await articles.get(database)
    
    if len(result) == 0:
        raise HTTPException(status_code=404, detail="Article not found")

    return result[0]
    
# todo: comments are not public!
# and could do with some joins/relationships to reduce number of network requests.
@router.get("/{id}/comments", response_class=JSONResponse)
async def get(id: int, r: Request, database: deps.Database):
    res = await articles.get_comments(database, id)
    return res
