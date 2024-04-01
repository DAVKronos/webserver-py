from databases import Database
import asyncio
import time
import json

async def process():
    N = 0
    
    values = []
    with open("tasks/photos2.json", "r") as fp:
            data = json.load(fp)
            for album in data:
                N = N + len(album)
                
                for photo in album:
                    id = photo['id']
                    url1 = photo['photo_url_original']
                    url2 = photo['photo_url_thumb']
                    values.append(f"({id},'{url1}','{url2}')")
    values = ','.join(values)

    database = Database("postgresql+asyncpg://localhost:5432/kronos_py_test", user="kronos_test", password="#FFMEe9#jq!!SmoW")
    await database.connect()
    t = time.time()
    async with database.transaction():
        # ALTER TABLE public.photos OWNER TO kronos_test;
        await database.execute("ALTER TABLE public.photos DROP COLUMN photo_url_original;")
        await database.execute("ALTER TABLE public.photos DROP COLUMN photo_url_thumb;")
        await database.execute("ALTER TABLE public.photos ADD photo_url_original varchar NULL;")
        await database.execute("ALTER TABLE public.photos ADD photo_url_thumb varchar NULL;")

        # UPDATE ... FROM is a 300x speed up on this dataset...
        # see: https://stackoverflow.com/questions/18797608/update-multiple-rows-in-same-query-using-postgresql
        # https://www.postgresql.org/docs/current/sql-update.html
        query = f"""UPDATE photos AS p SET
        photo_url_original = c.photo_url_original,
        photo_url_thumb = c.photo_url_thumb
        FROM (VALUES {values})
        AS c(id, photo_url_original,photo_url_thumb)
        WHERE c.id = p.id;"""
        await database.execute(query)
    
    print(f"Query done in: {(time.time()-t)*1000:.1f}ms. Updated {N} rows.")
    
if __name__ == "__main__":
    asyncio.run(process())

