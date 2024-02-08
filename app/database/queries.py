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

async def get_commissions(db):
    q = f"""select c.* FROM commissions as c;"""
    rows = await db.fetch_all(q)
    return [dict(r._mapping) for r in rows]

async def get_commissions_by_id(db, id: int):
    q = f"""select c.* FROM commissions as c WHERE id = {id};"""
    r = await db.fetch_one(q)
    return dict(r._mapping)

async def get_commission_memberships(db, id: int):
    q = f"""select c.*, u.name FROM commission_memberships as c
left join (select id, name from users) as u on u.id = c.user_id
where commission_id = {id};"""
    rows = await db.fetch_all(q)
    def nest(r):
        d = dict(r)
        d["user"]={"name":d["name"]}
        return d
    
    return [nest(r._mapping) for r in rows]

async def get_newsitems(db):
    q = f"""
select n.*, p.*, u.name, coalesce(comment_count, 0) comment_count from newsitems n
left join (	
	select commentable_id id, count(*) as comment_count from "comments" c
	where commentable_type = 'Newsitem'
	group by commentable_id
) c on c.id = n.id
left join (select id, name from users) as u on u.id = user_id
left join (select article_id, url_normal as articlephoto_url_normal, url_carrousel as articlephoto_url_carrousel from migrate_paperclip_articlephotos) as p on p.article_id = n.id;
"""
    rows = await db.fetch_all(q)

    def nest(r):
        d = dict(r)
        d["user"]={"name":d["name"]}
        return d
    
    return [nest(r._mapping) for r in rows]
