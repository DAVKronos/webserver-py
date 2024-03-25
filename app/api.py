from typing import Annotated
from fastapi import FastAPI, Request, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .routers import announcements, commissions, documents, events, photos, users
from .database.pg import get_database
from .database import queries

app = FastAPI()

app.include_router(announcements.router)
app.include_router(commissions.router)
app.include_router(documents.router)
app.include_router(events.router)
app.include_router(photos.router)
app.include_router(users.router)


@app.get("/pages", response_class=JSONResponse)
async def get_pages(r: Request, db: Annotated[dict, Depends(get_database)]):
    pass
#activities = await get_activities(db)
#    activities = activities[::-1][0:10]
#    return activitiesD
    #return JSONResponse(status_code=404, activities)

@app.get("/newsitems", response_class=JSONResponse)
async def get_newsitems(r: Request, db: Annotated[dict, Depends(get_database)]):
    res = await queries.get_newsitems(db)
    return [r for r in res if r["agreed"]]
