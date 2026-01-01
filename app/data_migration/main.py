### TO RUN THIS FILE: docker compose run --rm python python3 -m app.data_migration.main
import asyncio

from sqlalchemy import text
from ..database import create_ssh_engine

async def run_with_connection(func, old_db_name, new_db_name):
    with create_ssh_engine(old_db_name) as old_engine, \
         create_ssh_engine(new_db_name) as new_engine:
        async with old_engine.connect() as old_conn:
            async with new_engine.connect() as new_conn:
                await func(old_conn, new_conn)

async def migrate(old_conn, new_conn):
    await migrate_users(old_conn, new_conn)

async def migrate_users(old_conn, new_conn):
    result = await old_conn.execute(text("SELECT * FROM users"))
    rows = [dict(row) for row in result.mappings().all()]
    print(rows)

# Run the migration
# May need to empty the new database first
asyncio.run(run_with_connection(migrate, 'database_old', 'database'))