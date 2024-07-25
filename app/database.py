from databases import Database
from .config import config
from sqlalchemy.ext.asyncio import create_async_engine

def create_pool():
    return Database(
            f"postgresql+asyncpg://",
            # config.get('database.hostname', default)
            host = config['database']['hostname'],
            port = config['database']['port'],
            user=config['database']['username'],
            password=config['database']['password'],
            database = config['database']['database'],
            min_size = 1,
            max_size = 10
    )

def create_engine():
    return create_async_engine(
        f"postgresql+asyncpg://",
        connect_args = dict(
            # config.get('database.hostname', default)
            host = config['database']['hostname'],
            port = config['database']['port'],
            user=config['database']['username'],
            password=config['database']['password'],
            database = config['database']['database']),        
        echo=False,
        future=True
    )
