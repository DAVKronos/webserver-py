from .config import config
from sqlalchemy.ext.asyncio import create_async_engine
from sshtunnel import open_tunnel
from contextlib import contextmanager

@contextmanager
def create_engine():
    yield create_async_engine(
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

@contextmanager
def create_ssh_engine():
    with open_tunnel(
            ('kronos.nl', 22),
            ssh_username=config['database']['ssh']['username'],
            ssh_password=config['database']['ssh']['password'],
            remote_bind_address=('127.0.0.1', 5432),
            allow_agent = False,
            ssh_config_file = None) as con:
        
        engine = create_async_engine(
            f"postgresql+asyncpg://",
            connect_args = dict(
                # config.get('database.hostname', default)
                host = "127.0.0.1",
                port = con.local_bind_port,
                user=config['database']['username'],
                password=config['database']['password'],
                database = config['database']['database']),        
            echo=False,
            future=True
        )
        yield engine
