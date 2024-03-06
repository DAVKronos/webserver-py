from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, MetaData, String, Table
from .users import users
from .commissions import commissions

metadata = MetaData()

commission_memberships = Table(
    "commission_memberships",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(users.c.id)),
    Column("commission_id", Integer, ForeignKey(commissions.c.id)),
    Column("function", String),
    Column("installed", Boolean),
    Column("created_at", DateTime),
    Column("updated_at", DateTime)
)
