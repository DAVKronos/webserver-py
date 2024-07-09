from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, MetaData, String, Table

metadata = MetaData()

agendaitem_types = Table(
    "agendaitemtypes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name" , String),
    Column("name_en" , String)
)
