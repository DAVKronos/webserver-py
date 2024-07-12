from sqlalchemy import column, select, join, and_, func, text
from ..schemas import newsitems, comments,users

async def get_published(database, id: int = None):
    c = select(comments.c.commentable_id, func.count().label("comment_count")) \
        .group_by(comments.c.commentable_id) \
        .where(and_(comments.c.commentable_type=='Newsitem'))#
    
    if (id is not None): c = c.where(comments.c.commentable_id == id)
    c = c.subquery()
    query = select(newsitems, users.c.name.label("username"),
                   func.coalesce(text('comment_count'), 0).label("comment_count")) \
        .where(newsitems.c.agreed == True) \
        .join(c, newsitems.c.id== text('commentable_id'), isouter=True) \
        .join(users, newsitems.c.user_id == users.c.id, isouter=True) \
        .order_by(newsitems.c.created_at.desc())

    
    if id is not None: query = query.where(newsitems.c.id == id)
    
    rows = await database.fetch_all(query=query)
    
    def mapping(row):
        d = dict(row._mapping)
        u = d.pop('username')
        d.update({'user': {'name': u}})
        return d  
    return [mapping(r) for r in rows]

async def get_comments(database, id: int = None):
    q = select(comments).where(and_(comments.c.commentable_type=='Newsitem',
                                    comments.c.commentable_id == id))

    rows = await database.fetch_all(q)
    return rows
