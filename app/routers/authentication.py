from typing import Annotated
from fastapi import APIRouter, Form, Depends
from fastapi.responses import HTMLResponse, JSONResponse, Response
from ..models import authentication
from ..dependencies import DepDatabase

router = APIRouter(prefix="/auth")

@router.post("/login")
async def login(username: Annotated[str, Form()] , password:Annotated[str, Form()], database: DepDatabase, response: Response):
    token = await authentication.login(database, username, password)
    # log login attempt by
    if token is None:
        # log login result
        return Response("", 403)
    else:
        # log login result
        response = Response("", 200)
        response.set_cookie(key="login_token", value=token, max_age=3600*24*30, secure=True, httponly=True,)
        #response.set_cookie(key="session_token", value=token, secure=True, httponly=True,)
        return response

@router.post("/logout")
async def logout():
    # requires valid session
    # remove the session from cache
    # remove the session cookie
    return Response(200)

@router.post("/register")
async def register():
    return Response(200)

@router.post("/forgot-password")
async def forgot_password():
    # generate temporary login token (validity xx hours)
    # add field {can_reset_password: true}
    # lookup user in db if last_reset is more than some time ago: set it to now() and return succes,
    # send email
    # 
    return Response(200)

@router.post("/reset-password")
async def reset_password():
    # requires valid token that  has {can_reset_password:true }
    return Response(200)

@router.post("/request-verify-token")
async def request_verify_token():
    return Response(200)

@router.post("/verify")
async def verify():
    return Response(200)


