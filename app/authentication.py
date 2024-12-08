from typing import Annotated
import time
from datetime import datetime, timezone, timedelta
from passlib.context import  CryptContext
from jose import JWTError, jwt


from .models.user import User
from .config import config

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

async def decode_token(payload):#: Annotated[str]):
    #try:
        #except JWTError:
    user_id: str = payload.get("sub")
    if user_id is None:
        return false
    else:
        return User(id=int(user_id))

async def login(database, username, password):
    query = select(User) \
        .where(func.lower(column("email")) == func.lower(username))
    
    user = (await database.exec(query)).first()

    if not user:
        return None
    if not verify_password(password, user.encrypted_password):
        return None

    return create_token(str(user.id))

    
def logout():
    pass


def register():
    pass


def forgot_password_token():
    # check of user exists 
    # generate token
    pass

def verify_reset_password():
    # check token validity
    pass


def request_verify_token():
    pass
    # create token

async def verify():
    pass
    # verify token
    # and mark user as mail verified


