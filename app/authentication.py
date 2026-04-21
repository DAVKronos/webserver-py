from typing import Annotated, Optional
from datetime import datetime, timezone, timedelta
from passlib.context import  CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from pydantic import BaseModel, ValidationError
from .models.user import User
from .config import config
from sqlmodel import select, func, column
from .dependencies import Database
from .permissions import get_user_permissions, UserContext

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

def create_token(user: User):
    secret = config["authentication"]["jwt"]["secret"]
    algo = config["authentication"]["jwt"]["algorithm"]
    expires = config["authentication"]["access_token"]["expiration_minutes"]

    e = datetime.now(timezone.utc) + timedelta(minutes=expires)

    # We will probably not use JWT token, but for now, give an empty token list
    payload = {"sub": str(user.id), "scopes": [], "exp": int(e.timestamp())}
    
    token = jwt.encode(payload, secret, algorithm=algo)
    return token

async def validate_token(token):
    secret = config["authentication"]["jwt"]["secret"]
    algo = config["authentication"]["jwt"]["algorithm"]
    try:
        payload = jwt.decode(token, secret, algorithms=[algo])
    except JWTError as e:
        print(e)
        return None
    
    return payload

async def login(database, username, password):
    query = select(User) \
        .where(func.lower(column("email")) == func.lower(username))
    
    user: User = (await database.exec(query)).first()

    if not user:
        return None
    if not verify_password(password, user.encrypted_password):
        return None
    
    token = create_token(user) 

    return token


async def get_current_user(
    database: Database, 
    security_scopes: SecurityScopes, 
    token: Annotated[str, Depends(oauth2_scheme_required)]
) -> UserContext:
    try:
        payload = await validate_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid or expired token."
            )
        
        # Get user
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
        user = await database.get(User, int(user_id))
        if not user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="User not found")

        permissions = await get_user_permissions(user, database)
        return UserContext(user, permissions)
    except (JWTError, ValidationError, ValueError) as e:
        print(e)
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
        #  Validate token
        payload = await validate_token(token)
        if not payload:
            return None
        
        # Get User
        user_id = payload.get("sub")
        if not user_id:
            return None
        user = await database.get(User, int(user_id))
        if not user:
            return None

        # Get scopes
        permissions = await get_user_permissions(user, database)

        return UserContext(user, permissions)
        # return user

    except Exception:
        return None
