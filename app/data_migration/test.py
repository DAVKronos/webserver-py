import asyncio

from sqlalchemy import text
from ..database import create_ssh_engine

async def run_with_connection(func, old_db_name, new_db_name):
    with create_ssh_engine(old_db_name) as old_engine, \
         create_ssh_engine(new_db_name) as new_engine:
        async with old_engine.connect() as old_conn:
            async with new_engine.connect() as new_conn:
                await func(old_conn, new_conn)

# Test function 
async def print_users(old_conn, new_conn):
    result = await old_conn.execute(text("SELECT * FROM users"))
    rows = [dict(row) for row in result.mappings().all()]
    print(rows)


asyncio.run(run_with_connection(print_users, 'database_old'))