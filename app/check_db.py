"""Checks that this image can reach the database, the same way the app does on startup.

    python -m app.check_db

Opens the engine (through the SSH tunnel when config.toml has [database.ssh]) and runs
`SELECT 1`. Reads nothing and changes nothing. Exits non-zero with the error if it fails.
"""
import asyncio
import sys

from sqlalchemy import text

from . import database
from .config import config


async def select_one(engine):
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))
    await engine.dispose()


def main():
    via_ssh = "ssh" in config["database"]
    create_engine = database.create_ssh_engine if via_ssh else database.create_engine
    try:
        with create_engine() as engine:
            asyncio.run(select_one(engine))
    except Exception as error:
        print(f"Database check failed ({'SSH tunnel' if via_ssh else 'direct'}): {type(error).__name__}: {error}", file=sys.stderr)
        raise
    print(f"Database check passed ({'SSH tunnel' if via_ssh else 'direct'}).")


if __name__ == "__main__":
    main()
