import uvicorn
from typing import Annotated
from fastapi import FastAPI, Request, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# from .admin import admin
from . import api
from .routers import users
from .database.pg import get_database
from .database.queries import *

# add csrf middleware
import jinja2

app = FastAPI()
app.mount("/api/v1", api.app)
# app.mount("/admin", admin.app)
# app.include_router(users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# @app.get("/activity/{id}", response_class=HTMLResponse)
@app.get("/activity/{id}")
async def activity(id: int, r: Request, db: Annotated[dict, Depends(get_database)]):
    res = await get_activities_by_id(db, id)
    return res
    # return HTMLResponse(f"<turbo-frame id='activity-{id}'>{res['description']}</turbo-frame>")


@app.get("/", response_class=HTMLResponse)
async def home(r: Request):
    return templates.TemplateResponse(name="react.html", context={"request": r})


if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run("app.main:app", reload=True, host="0.0.0.0", port=8000)
