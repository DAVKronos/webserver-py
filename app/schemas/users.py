from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, MetaData, String, Table
from .user_types import user_types

metadata = MetaData()

users= Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", DateTime),
    Column("updated_at", DateTime),
    Column("user_type_id", Integer, ForeignKey(user_types.c.id)),
    Column("name", String),
    Column("initials", String),
    Column("email", String),
    Column("encrypted_password", String)
)
