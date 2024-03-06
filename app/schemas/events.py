from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, MetaData, String, Table
from .eventtypes import eventtypes
from .agendaitems import agendaitems

metadata = MetaData()

events = Table(
    "events",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("date", DateTime),
    Column("eventtype_id", Integer, ForeignKey(eventtypes.c.id)),
    Column("agendaitem_id", Integer, ForeignKey(agendaitems.c.id)),
    Column("distance", Float),
    Column("created_at", DateTime),
    Column("updated_at", DateTime)
)
