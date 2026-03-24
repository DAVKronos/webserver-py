############### UPDATED #################
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from ..user import UserResponse

############ MAILING LIST
class MailingListBase(SQLModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    local_part: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class MailingListResponse(MailingListBase):
    pass

################ MAILING LIST MEMBERSHIPS

class MailingListMemberBase(SQLModel):
    id: int
    user_id: Optional[int] = None
    mailing_list_id: Optional[int] =None 
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class MailingListMemberResponse(MailingListMemberBase):
    user: "UserResponse"
    mailing_list: "MailingListResponse"
