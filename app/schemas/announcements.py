from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, MetaData, String, Table

metadata = MetaData()

announcements = Table(
    "announcements",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("message", String()),
    Column("title", String()),
    Column("url", String()),
    Column("starts_at", DateTime()),
    Column("ends_at", DateTime())
)
