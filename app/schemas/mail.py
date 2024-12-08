from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, MetaData, String, Table

metadata = MetaData()

aliases = Table(
    "aliases",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("created_at", DateTime),
    Column("updated_at", DateTime),
    Column("name", String),
    Column("emailaddress", String),
    Column("description", String)
)
aliases_mailinglists = Table(
    "aliases_mailinglists"
    metadata,
    Column("alias_id", Integer, ForeignKey()),
    Column("mailinglist_id", Integer, ForeignKey())
)
mailinglists = Table(
    "mailinglists",
    metadata,
    Column("id", Integer),
    Column("commission_id", Integer, ForeignKey()),
    Column("created_at", DateTime),
    Column("updated_at", DateTime),
    Column("name", String),
    Column("description", String),
    Column("local_part", String)
)
mailinglist_memberships = Table(
    "mailinglist_memberships",
    metadata,
   Column("id", Integer),
    Column("created_at", DateTime),
    Column("updated_at", DateTime),
    Column("user_id", Integer, ForeignKey()),
    Column("mailinglist_id", Integer, ForeignKey()),
 
 
)
