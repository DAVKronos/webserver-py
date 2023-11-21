from pydantic import BaseModel
from ..database import *

# , EmailStr


class UserIn(BaseModel):
    username: str
    password: str
    # email: EmailStr
    full_name: str | None = None


class User(BaseModel):
    pass


def fake_save_user(user_in: UserIn):
    # hashed_password = fake_password_hasher(user_in.password)
    hashed_password = "fafa"

    user_in_db = UserIn(**user_in.dict(), hashed_password=hashed_password)
    print(user_in_db.model_dump())
    return user_in_db


def list():
    pass


def read():
    # @classmethod
    # def read(cls,id:str):
    # user = cls(**record)
    User(**record)
    pass


def create():
    pass


def update():
    pass


def delete():
    pass
