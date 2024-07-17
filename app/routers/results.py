from typing import Annotated
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from ..dependencies import DepDatabase
from ..queries import results

router = APIRouter(prefix="/results")

@router.get("/", response_class=JSONResponse)
async def get(r: Request, database: DepDatabase):
    res = await results.get(database)
    return res

