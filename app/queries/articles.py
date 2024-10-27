from sqlmodel import select, func, and_, text
from app.models import Article, ArticlePublic, ArticlePublicWithCommentCount, Comment, User, UserPublic

async def get_comments(database, id):
    query = select(Comment) \
        .where(and_(Comment.commentable_type=='Newsitem',
                    Comment.commentable_id == id))

    result = (await database.exec(query)).all()
    return result
