from sqlmodel import select, func, and_, text
from app.models import Article, ArticlePublic, ArticlePublicWithCommentCount, Comment, User, UserPublic


async def get(database, id: int = None):
    subq = select(Comment.commentable_id, func.count().label("comment_count")) \
        .group_by(Comment.commentable_id) \
        .where(and_(Comment.commentable_type=='Newsitem')) \
        .subquery()
    
    query = select(Article, func.coalesce(text('comment_count'), 0).label("comment_count")) \
        .where(Article.agreed == True) \
        .join(subq, Article.id == text('commentable_id'), isouter=True) \
        .order_by(Article.created_at.desc())
    if id is not None:
        query = query.where(Article.id == id)
    
    result = (await database.exec(query)).all()

    return [ArticlePublicWithCommentCount(**record[0].dict(), user=UserPublic(**record[0].user.dict()) if record[0].user is not None else None, comment_count=record[1]) for record in result]


async def get_comments(database, id):
    query = select(Comment) \
        .where(and_(Comment.commentable_type=='Newsitem',
                    Comment.commentable_id == id))

    result = (await database.exec(query)).all()
    return result
