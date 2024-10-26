from typing import Annotated
from fastapi import FastAPI, Depends, Header, HTTPException, Request
from databases.core import Connection
from .models.user import User
from .models import authentication
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import config

async def get_async_session(request: Request) -> AsyncSession:
   async_session = sessionmaker(bind=request.app.state.engine, class_=AsyncSession, expire_on_commit=False)
   async with async_session() as session:
       yield session

Database = Annotated[AsyncSession, Depends(get_async_session)]
       
#async def get_database(database: Annotated[str, Header()]):
#    if x_token != "fake-super-secret-token":
#        raise HTTPException(status_code=400, detail="X-Token header invalid")
#from .main import app
async def get_database(request: Request):
    pool = request.app.state.connection_pool
    async with pool.connection() as connection:
       yield connection

DepDatabase = Annotated[Connection, Depends(get_database)]

async def jwt_onetime_parameter():
    # inject a decoded jwt token into the request,
    # and set an encoded jwt token if it is set in the response
    # fail if the secret is not strong enough
    pass

async def get_active_user(request: Request, database: Database):
    token = request.cookies["v2-access-token"]
    payload = await authentication.validate_token(token)
    user = await authentication.decode_token(payload)
    # TODO: now we hit the database on every request to lookup the user. Maybe be smarter about our JWT token. 
    user = await database.get(User, user.id)
    
    return user

ActiveUser = Annotated[User, Depends(get_active_user)]