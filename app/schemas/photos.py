from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, MetaData, String, Table
from .agendaitems import agendaitems

metadata = MetaData()

photo_albums = Table(
    "photoalbums",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", DateTime),
    Column("updated_at", DateTime),
    Column("agendaitem_id", Integer, ForeignKey(agendaitems.c.id)),
    Column("public", Boolean),
    Column("name", String),
    Column("name_en", String),
    Column("eventdate", DateTime),
    Column("url", String)
)
photos = Table(
    "photos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", DateTime),
    Column("updated_at", DateTime),
    Column("photoalbum_id", Integer, ForeignKey(photo_albums.c.id)),
    Columns("processing", Boolean),
    Columns("exif_date", DateTime),
    Columns("youtube_id", String),
    Columns("caption", String),
    Column("photo_file_name", String),
    Column("photo_content_type", String),
    Column("photo_file_size", Integer),
    Column("photo_updated_at", DateTime)
)
    
