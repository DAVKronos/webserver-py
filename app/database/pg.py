from databases import Database


async def get_database():
    async with Database(
            "postgresql+asyncpg://kronos_test@localhost:5432/kronos_py_test",
            password="#FFMEe9#jq!!SmoW"
    ) as db:
        yield db

        
