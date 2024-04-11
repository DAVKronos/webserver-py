from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, MetaData, String, Table

metadata = MetaData()
pages = Table(
    "pages",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", DateTime),
    Column("updated_at", DateTime),
    Column("public", Boolean),
    Column("highlight", Boolean),
    Column("sort_order", Integer),
    Column("information" , String),
    Column("information_en" , String),
    Column("pagetag" , String),
    Column("pagetag_en" , String),
    Column("menu" , String)
)

