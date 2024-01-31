from typing import Annotated
from fastapi import FastAPI, Request, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .routers import users
from .database.pg import get_database
from .database.queries import *

app = FastAPI()


@app.get("/pages", response_class=JSONResponse)
async def get_pages(r: Request, db: Annotated[dict, Depends(get_database)]):
    activities = await get_activities(db)
    activities = activities[::-1][0:10]
    return activities
