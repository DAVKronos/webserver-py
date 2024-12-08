from fastapi import FastAPI
from .routers import activities, announcements, articles, commissions, documents, events, pages, photos, users, results

app = FastAPI()

app.include_router(activities.router)
app.include_router(announcements.router)
app.include_router(articles.router)
app.include_router(commissions.router)
app.include_router(documents.router)
app.include_router(events.router)
app.include_router(pages.router)
app.include_router(photos.router)
app.include_router(results.router)
app.include_router(users.router)
