from typing import Annotated, Optional
from datetime import datetime, timezone, timedelta
from passlib.context import  CryptContext
from jose import JWTError, jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from pydantic import BaseModel, ValidationError
from .models.user import User
from .config import config
from sqlmodel import select, func, column
from .dependencies import Database

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []

oauth2_scheme_required = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scopes={"public": ""},
    auto_error=True
)

oauth2_scheme_optional = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scopes={"public": ""},
    auto_error=False
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

    # TODO: scopes vullen obv user_type / commissie lidmaatschap
    scopes = ["public", "user", "admin"]
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



async def get_current_user(
    database: Database, 
    security_scopes: SecurityScopes, 
    token: Annotated[str, Depends(oauth2_scheme_required)]
) -> User:
    try:
        payload = await validate_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid or expired token."
            )
        
        user_id = payload.get("sub")
        token_scopes = payload.get("scopes", [])

        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        user = await database.get(User, int(user_id))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
        # Check permissions
        for scope in security_scopes.scopes:
            if scope not in token_scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions"
                )
        
        return user

    except (JWTError, ValidationError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_optional_user(
    database: Database, 
    token: Annotated[Optional[str], Depends(oauth2_scheme_optional)]
) -> Optional[User]:
    # returning None means guest mode (not logged in)
    if not token:
        return None
    
    try:
        payload = await validate_token(token)
        if not payload:
            return None
            
        user_id = payload.get("sub")
        if not user_id:
            return None

        user = await database.get(User, int(user_id))
        return user # returns User if found, None otherwise

    except Exception:
        return None
