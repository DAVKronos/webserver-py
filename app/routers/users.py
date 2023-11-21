from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from ..models.user import *

router = APIRouter(prefix="/users")


@router.get("/", tags=["users"], response_class=JSONResponse)
async def read():
    # list_users_query()
    fake_save_user(UserIn(username="foo", password="bar"))
    return HTMLResponse("<b>foo bar</b>")


@router.get("/active", tags=["users"], response_class=HTMLResponse)
async def active():
    fake_save_user(UserIn(username="foo", password="bar"))
    # return TurboFrame('active-users',)
    return HTMLResponse(f'<turbo-frame id="active-users">ussss</turbo-frame>')
