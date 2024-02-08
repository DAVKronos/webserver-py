from databases import Database
from ..config import config

async def get_database():
    async with Database(
            f"postgresql+asyncpg://{config['database']['username']}@{config['database']['hostname']}:{config['database']['port']}/{config['database']['database']}",
            password=config['database']['password'],
    ) as db:
        yield db

        
