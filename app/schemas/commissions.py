from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, MetaData, String, Table

metadata = MetaData()

commissions = Table(
    "commissions",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("name_en", String),
    Column("description", String),
    Column("description_en", String),
    Column("email", String),
    Column("role", String),
    Column("created_at", DateTime),
    Column("updated_at", DateTime),
)    
