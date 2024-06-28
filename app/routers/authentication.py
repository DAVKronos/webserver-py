from typing import Annotated
from fastapi import APIRouter, Form, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from ..models import authentication
from ..dependencies import DepDatabase
from ..config import config

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
        response.set_cookie(key="v2-access-token", value=token, max_age=3600*24*30, secure=True, httponly=True,)
        response.headers["access-token"] = token
        return response

@router.post("/logout")
async def logout():
    # requires valid session
    # remove the session from cache
    # remove the session cookie
    return Response(200)


# class JWTMiddleware that will renew an access token / set a session token

class PermissionCheck:
    def __init__(self, required_scopes: [str]):
        self.required_scopes = required_scopes
    async def __call__(self, request: Request):
        data = request.cookies["v2-access-token"]
        token = await authentication.validate_token(data)
        user_scopes = token["scopes"]

        check = all(s in user_scopes for s in self.required_scopes)
        print(check, user_scopes, self.required_scopes)
        
        
@router.get("/scope")
async def validate_scope(user: Annotated[str, Depends(PermissionCheck(config['permissions']['scopes']['test']))]):
    return Response("",200)

@router.get("/validate-token")
async def validate(request: Request):
    token = request.cookies["v2-access-token"]
    await authentication.validate_token(token)
    
    return Response("", 200)


# maybe this belongs more to user administration than authentication?
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

