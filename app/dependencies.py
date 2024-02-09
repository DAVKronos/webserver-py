from typing import Annotated
from fastapi import Header, HTTPException

async def get_database(database: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

