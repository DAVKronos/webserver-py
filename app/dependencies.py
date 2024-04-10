from typing import Annotated
from fastapi import FastAPI, Depends, Header, HTTPException, Request
from databases.core import Connection

#async def get_database(database: Annotated[str, Header()]):
#    if x_token != "fake-super-secret-token":
#        raise HTTPException(status_code=400, detail="X-Token header invalid")
#from .main import app
async def get_database(request: Request):
    pool = request.app.state.connection_pool
    async with pool.connection() as connection:
        yield connection

DepDatabase = Annotated[Connection, Depends(get_database)]
