from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, MetaData, String, Table

metadata = MetaData()

folders = Table(
    "folders",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("folder_id", Integer)
)
kronometers = Table(
    "kronometers",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", DateTime),
    Column("updated_at", DateTime),
    Column("folder_id", Integer, ForeignKey(folders.c.id)),
    Column("public", Boolean),
    Column("name", String),
    Column("date", DateTime),
    Column("file_file_name", String),
    Column("file_content_type", String),
    Column("file_file_size", Integer),
    Column("file_updated_at", DateTime)
)
