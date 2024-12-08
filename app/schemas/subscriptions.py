from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, MetaData, String, Table

metadata = MetaData()


subscriptions = Table(
    "subscriptions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", DateTime),
    Column("updated_at", DateTime),
    Column("agendaitem_id", Integer),
    Column("user_id", Integer),
    Column("name", String),
    Column("comment", String),
    Column("reserve", Boolean),
)
