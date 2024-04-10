
import uvicorn
from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import FastAPI, Request, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    async with database.create_pool() as pool:
        api.app.state.connection_pool = pool
        app.state.connection_pool = pool
        yield

app = FastAPI(lifespan=lifespan)
# from .admin import admin
from . import api, database
from .config import config

# add csrf middleware
import jinja2
templates = Jinja2Templates(directory="templates")

app.mount("/api/v1", api.app)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_home(r: Request):
    return templates.TemplateResponse(name="react.html", context={"request": r})

if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    r = config["uvicorn"]["reload"]
    h = config["uvicorn"]["hostname"]
    p = config["uvicorn"]["port"]
    uvicorn.run("app.main:app", reload=r, host=h, port=p)
