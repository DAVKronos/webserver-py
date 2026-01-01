import asyncio

from sqlalchemy import text
from ..database import create_ssh_engine

async def run_with_connection(func, database_name):
    with create_ssh_engine(database_name) as engine:
        async with engine.connect() as conn:
            await func(conn)

# Test function 
async def print_users(conn):
    result = await conn.execute(text("SELECT * FROM users"))
    rows = [dict(row) for row in result.mappings().all()]
    print(rows)


asyncio.run(run_with_connection(print_users, 'database_old'))