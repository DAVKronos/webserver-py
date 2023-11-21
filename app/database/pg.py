from databases import Database


async def get_database():
    async with Database(
        "postgresql+asyncpg://postgres:kronos@localhost:5432/kronos_production"
    ) as db:
        yield db
