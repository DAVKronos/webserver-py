from databases import Database
import asyncio
import time

async def req():
    from requests import get
    data = get("https://kronos.nl/api/v1/newsitems.json").json()

    N = 0
    rows = []
    for d in data:
        N = N + 1
        id = d['id']
        url1 = d['articlephoto_url_normal']
        url2 = d['articlephoto_url_carrousel']
        rows.append(f"({id},'{url1}','{url2}')")
    rows = ','.join(rows)
    
    database = Database("postgresql+asyncpg://localhost:5432/kronos_py_test", user="kronos_test", password="#FFMEe9#jq!!SmoW")
    await database.connect()
     
    t = time.time()
    async with database.transaction():
        await database.execute("ALTER TABLE public.newsitems DROP COLUMN articlephoto_url_normal;")
        await database.execute("ALTER TABLE public.newsitems DROP COLUMN  articlephoto_url_carrousel;")
        await database.execute("ALTER TABLE public.newsitems ADD articlephoto_url_normal varchar NULL;")
        await database.execute("ALTER TABLE public.newsitems ADD articlephoto_url_carrousel varchar NULL;")
        query = f"""UPDATE public.newsitems AS tbl SET
        articlephoto_url_normal = val.url1,
        articlephoto_url_carrousel = val.url2
        FROM (VALUES {rows})
        AS val(id, url1, url2)
        WHERE val.id = tbl.id;"""
        res = await database.execute(query)
        print(res)
    print(f"Query done in: {(time.time()-t)*1000:.1f}ms. Updated {N} rows.")
    
    
if __name__ == "__main__":
    asyncio.run(req())

