async def get_news(db):
    # q = """CREATE TABLE Users (id INTEGER PRIMARY KEY, name VARCHAR(100), status INTEGER)"""
    # await database.execute(query=q)
    q = "SELECT id, title, news, articlephoto_file_name FROM newsitems"
    rows = await db.fetch_all(q)
    return [dict(r._mapping) for r in rows]


async def get_activities(db):
    q = "SELECT id, name, description, date FROM agendaitems"
    rows = await db.fetch_all(q)
    return [dict(r._mapping) for r in rows]


async def get_activities_by_id(db, id):
    q = f"SELECT id, name, description, date FROM agendaitems WHERE id = {id}"
    r = await db.fetch_one(q)
    return dict(r._mapping)
