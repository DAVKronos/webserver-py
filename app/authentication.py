from typing import Annotated
import time
from datetime import datetime, timezone, timedelta
from passlib.context import  CryptContext
from jose import JWTError, jwt
from fastapi import Depends, FastAPI, HTTPException, Request, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from pydantic import BaseModel, ValidationError
from .models.user import User
from .config import config
from .dependencies import Database

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"public": ""}
)

def verify_password(password, hashed_password):
    return crypt.verify(password, hashed_password)

def hash_password(password):
    return crypt.hash(password)

def create_token(user):
    secret = config["authentication"]["jwt"]["secret"]
    algo = config["authentication"]["jwt"]["algorithm"]
    expires = config["authentication"]["access_token"]["expiration_minutes"]

    e = datetime.now(timezone.utc) + timedelta(minutes=expires)

    scopes = ["kronos_user"]
    # user, contributor, board, admin
    payload = {"sub": user, "scopes": scopes, "exp": int(e.timestamp())}
    
    token = jwt.encode(payload, secret, algorithm=algo)
    return token

async def validate_token(token):
    secret = config["authentication"]["jwt"]["secret"]
    algo = config["authentication"]["jwt"]["algorithm"]
    try:
        payload = jwt.decode(token, secret, algorithms=[algo])
    except JWTError:
        payload = None
    
    return payload

async def login(database, username, password):
    query = select(User) \
        .where(func.lower(column("email")) == func.lower(username))
    
    user = (await database.exec(query)).first()

    if not user:
        return None
    if not verify_password(password, user.encrypted_password):
        return None

    return create_token(str(user.id))

# TODO: rename to something more explanatory
async def current_user(database: Database, scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    payload = await validate_token(token)
    user_id: str = payload.get("sub")
    scopes: str = payload.get("scopes")

    user = await database.get(User, int(user_id))
    # return TokenData(scopes=scopes, username=username)
    return user
    
