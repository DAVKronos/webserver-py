from sqlmodel import Field, Relationship,  SQLModel
from datetime import datetime

class MailinglistMembershipBase(SQLModel):
    id: int | None
    created_at: datetime | None
    updated_at: datetime | None


class MailinglistMembershipResponse(MailinglistMembershipBase):
    pass

class MailinglistMembership(MailinglistMembershipBase, table=True):
    __tablename__: str = "mailinglist_memberships"
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None
    mailinglist_id: int | None
