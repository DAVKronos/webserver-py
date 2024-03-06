from sqlalchemy import Boolean, Column, DateTime, Numeric, ForeignKey, Integer, MetaData, String, Table

from .events import events
from .users import users

metadata = MetaData()

results = Table(
    "results",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("result", String),
    Column("username", String),
    Column("calculated", Numeric),
    Column("wind", Numeric),
    Column("place", Integer),
    Column("event_id", Integer, ForeignKey(events.c.id)),
    Column("user_id", Integer, ForeignKey(users.c.id)),
)
