from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, MetaData, String, Table

metadata = MetaData()
newsitems = Table(
    "newsitems",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("title_en", String),
    Column("news", String),
    Column("news_en", String),
    Column("agreed", Boolean),
    Column("user_id", Integer),
    Column("agreed_by", Integer),
    Column("articlephoto_updated_at", DateTime),
    Column("articlephoto_url_normal", String),
    Column("articlephoto_url_carrousel", String),
    Column("created_at", DateTime),
    Column("updated_at", DateTime),
)
