############### UPDATED #################
from typing import Optional, TYPE_CHECKING
from datetime import datetime, date
from sqlmodel import SQLModel

# Resolve circular imports
if TYPE_CHECKING:
    from .file import FileResponse


################ USERS
class UserBase(SQLModel):
    id: int
    name: Optional[str] = None
    initials: Optional[str] = None
    email: Optional[str] = None
    birthdate: Optional[date] = None
    address: Optional[str] = None
    postalcode: Optional[str] = None
    city: Optional[str] = None
    sex: Optional[str] = None
    allow_password_change: Optional[bool] = None
    avatar_file_id: Optional[int] = None
    phonenumber: Optional[str] = None
    user_type_id: Optional[int] = None
    bank_account_number: Optional[str] = None
    unioncard_number: Optional[str] = None
    institution: Optional[str] = None
    joined_in: Optional[int] = None
    confirmed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    user_type: Optional["UserTypeResponse"] = None
    avatar_file: Optional["FileResponse"] = None


################# USER TYPES

class UserTypeBase(SQLModel):
    id: int
    name_nl: Optional[str] = None
    name_en: Optional[str] = None
    is_donor: Optional[bool] = None
    is_competition: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserTypeResponse(UserTypeBase):
    pass

######### PASSWORD ACTIONS

class ResetPasswordActionBase(SQLModel):
    id: int
    user_id: Optional[int] = None
    token: Optional[str] = None
    sent_at: Optional[datetime] = None
    remember_created_at: Optional[datetime] = None


class ResetPasswordActionResponse(ResetPasswordActionBase):
    pass