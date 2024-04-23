from typing import Annotated

from passlib.context import  CryptContext
from jose import JWTError, jwt

from ..queries import users
from datetime import datetime, timezone, timedelta
from ..config import config

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(password, hashed_password):
    return crypt.verify(password, hashed_password)

def hash_password(password):
    return crypt.hash(password)

def create_token(user):
    secret = config["authentication.jwt"]["secret"]
    algo = config["authentication.jwt"]["algorithm"]
    expires = config["authentication.jwt"]["expiration_minutes"]

    e = datetime.now(timezone.utc) + timedelta(minutes=expires)
    payload = {"sub": user, "expires": e}
    
    token = jwt.encode(payload, secret, algorithm=algo)
    return token

async def decode_token(token):#: Annotated[str]):
    #try:
        #except JWTError:
    username: str = payload.get("sub")
    if username is None:
        return false

async def get_active_user():
    pass


async def login(database, username, password):
    user = await users.get_password(database, username)
    print(user)
    if not user:
        return None
    if not verify_password(password, user.encrypted_password):
        return None
    return create_token(user)

    
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


