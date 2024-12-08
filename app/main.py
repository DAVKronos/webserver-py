from typing import Annotated
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .routers import authentication
from .config import config

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_engine_fn = database.create_ssh_engine if ("ssh" in config["database"]) else database.create_engine
    
    with create_engine_fn() as engine:
        print("engine:", engine)
        api.app.state.engine = engine
        app.state.engine = engine
        yield

app = FastAPI(lifespan=lifespan)
# from .admin import admin
from . import api, database

# add csrf middleware
import jinja2
templates = Jinja2Templates(directory="templates")

app.mount("/api/v1", api.app)
app.mount("/static", StaticFiles(directory="static", follow_symlink=True), name="static")
app.include_router(authentication.router)

@app.get("/{full_path:path}", response_class=HTMLResponse)
async def get_home(r: Request, full_path: str):
    return templates.TemplateResponse(name="react.html", context={"request": r})

if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    r = config["uvicorn"]["reload"]
    h = config["uvicorn"]["hostname"]
    p = config["uvicorn"]["port"]
    ph = config["uvicorn"]["proxy_headers"]
    
    uvicorn.run("app.main:app", reload=r, host=h, port=p, proxy_headers=ph)
