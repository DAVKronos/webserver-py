from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, MetaData, String, Table

metadata = MetaData()

agendaitems = Table(
    "agendaitems",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("location", String),
)
