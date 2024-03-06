from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, MetaData, String, Table

metadata = MetaData()

users= Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("initials", String),
    Column("email", String),
    Column("created_at", DateTime),
    Column("updated_at", DateTime),
)
