from fastapi import FastAPI

from .routers import agendaitems, announcements, committees, documents, news_items, pages, photos, users, user_types

app = FastAPI()

app.include_router(agendaitems.router)
app.include_router(announcements.router)
app.include_router(news_items.router)
# app.include_router(committees.router)
# app.include_router(documents.router)
app.include_router(pages.router)
# app.include_router(photos.router)
app.include_router(users.router)
# app.include_router(user_types.router)
