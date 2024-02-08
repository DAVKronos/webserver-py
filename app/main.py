import uvicorn
from typing import Annotated
from fastapi import FastAPI, Request, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# from .admin import admin
from . import api
from .config import config
from .routers import users
from .database.pg import get_database
from .database.queries import *

# add csrf middleware
import jinja2

app = FastAPI()
app.mount("/api/v1", api.app)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_home(r: Request):
    return templates.TemplateResponse(name="react.html", context={"request": r})


if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    r = config["uvicorn"]["reload"]
    h = config["uvicorn"]["hostname"]
    p = config["uvicorn"]["port"]
    uvicorn.run("app.main:app", reload=r, host=h, port=p)
