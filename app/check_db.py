"""Checks that this image can reach the database, the same way the app does on startup.

    python -m app.check_db            connect and run SELECT 1
    python -m app.check_db --tables   also read one row from every table the app uses

Opens the engine (through the SSH tunnel when config.toml has [database.ssh]). Only reads;
never changes anything. Exits non-zero with the error if a check fails.
"""
import asyncio
import sys

from sqlalchemy import text
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.main import default_registry

from . import api, database  # noqa: F401  (api imports every router, which registers every model)
from .config import config


async def select_one(engine):
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))


async def check_tables(engine):
    """Reads one row per model the way the app does, so a missing table or column shows up here."""
    failures = 0
    models = sorted((m.class_ for m in default_registry.mappers), key=lambda model: model.__tablename__)
    async with AsyncSession(engine) as session:
        for model in models:
            try:
                (await session.exec(select(model).limit(1))).all()
                print(f"  ok    {model.__tablename__}")
            except Exception as error:
                failures += 1
                first_line = str(error).splitlines()[0] if str(error) else ""
                print(f"  FAIL  {model.__tablename__}: {type(error).__name__}: {first_line}")
                await session.rollback()
    return failures


async def run(engine, tables):
    try:
        await select_one(engine)
        return await check_tables(engine) if tables else 0
    finally:
        await engine.dispose()


def main():
    tables = "--tables" in sys.argv[1:]
    route = "SSH tunnel" if "ssh" in config["database"] else "direct"
    create_engine = database.create_ssh_engine if route == "SSH tunnel" else database.create_engine
    try:
        with create_engine() as engine:
            failures = asyncio.run(run(engine, tables))
    except Exception as error:
        print(f"Database check failed ({route}): {type(error).__name__}: {error}", file=sys.stderr)
        raise
    if failures:
        print(f"Database reachable ({route}), but {failures} table(s) failed.", file=sys.stderr)
        sys.exit(1)
    print(f"Database check passed ({route}).")


if __name__ == "__main__":
    main()
