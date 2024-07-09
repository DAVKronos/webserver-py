from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, MetaData, String, Table
from .agendaitem_types import agendaitem_types
metadata = MetaData()

agendaitems = Table(
    "agendaitems",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name" , String),
    Column("name_en" , String),
    Column("description" , String),
    Column("description_en" , String),
    Column("location" , String),
    Column("date", DateTime),
    Column("subscribe", Boolean),
    Column("subscriptiondeadline", DateTime),
    Column("commission_id", Integer),
    Column("category", String),
    Column("intern", Boolean),
    Column("agendaitemtype_id", Integer, ForeignKey(agendaitem_types.c.id)),
    Column("url", String),
    Column("user_id", Integer),
    Column("maxsubscription", Integer),
)
