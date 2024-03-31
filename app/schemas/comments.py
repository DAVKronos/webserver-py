from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, MetaData, String, Table
from .users import users
from .newsitems import newsitems
metadata = MetaData()
comments = Table(
    "comments",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(users.c.id)),
    Column("commenttext", String),
    Column("commentable_id", Integer),
    Column("commentable_type", String),
    Column("created_at", DateTime),
    Column("updated_at", DateTime)
)    

