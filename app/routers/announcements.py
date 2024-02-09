from typing import Annotated
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from ..database.pg import get_database
from ..queries import announcements
from datetime import datetime
router = APIRouter(prefix="/announcements")

@router.get("/current", response_class=JSONResponse)
async def get(r: Request, database: Annotated[dict, Depends(get_database)]):
    res = await announcements.get(database, active=datetime.now())
    return res

