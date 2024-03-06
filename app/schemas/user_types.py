from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, MetaData, String, Table

metadata = MetaData()

user_types = Table(
    "user_types",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", DateTime),
    Column("updated_at", DateTime),
    Column("name", String),
    Column("name_en", String),
    Column("donor", Boolean),
    Column("competition", Boolean)
)

