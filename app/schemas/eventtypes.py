from sqlalchemy import Boolean, Column, DateTime, Numeric, ForeignKey, Integer, MetaData, String, Table

metadata = MetaData()

eventtypes = Table(
    "eventtypes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("shortname", String),
    Column("formula", String),
    Column("female_formula", String),
    Column("measuringunit", String),
    Column("calculated_unit", String),
    Column("show_wind", Boolean),
    Column("important", Boolean),
    Column("distance", Numeric),
    Column("created_at", DateTime),
    Column("updated_at", DateTime)
)
