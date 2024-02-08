from typing import Annotated
from fastapi import FastAPI, Request, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .database.pg import get_database
from .database import queries

app = FastAPI()

@app.get("/pages", response_class=JSONResponse)
async def get_pages(r: Request, db: Annotated[dict, Depends(get_database)]):
    activities = await get_activities(db)
    activities = activities[::-1][0:10]
    return activities
    #return JSONResponse(status_code=404, activities)

@app.get("/commissions", response_class=JSONResponse)
async def get_commissions(r: Request, db: Annotated[dict, Depends(get_database)]):
    res = await queries.get_commissions(db)
    return res

@app.get("/commissions/{id}", response_class=JSONResponse)
async def get_commissions(id: int, r: Request, db: Annotated[dict, Depends(get_database)]):
    res = await queries.get_commissions_by_id(db, id)
    return res

@app.get("/commissions/{id}/commission_memberships", response_class=JSONResponse)
async def get_commission_memberships(id: int, r: Request, db: Annotated[dict, Depends(get_database)]):
    res = await queries.get_commission_memberships(db, id)
    return res


@app.get("/newsitems", response_class=JSONResponse)
async def get_newsitems(r: Request, db: Annotated[dict, Depends(get_database)]):
    res = await queries.get_newsitems(db)
    return [r for r in res if r["agreed"]]
