from sqlmodel import SQLModel, select
from typing import Union, Optional, Any, List
from .dependencies import Database
from .models.user import User
from .models.committees import Committee, CommitteeMember

class Ability(SQLModel):
    action: Union[str, list[str]]
    subject: Union[str, list[str]]
    conditions: Optional[object] = None
    inverted: Optional[bool] = None

class UserContext:
    user: User
    permissions: List[Ability]
    def __init__(self, user: User, permissions: List[Ability]):
        self.user = user
        self.permissions = permissions

def can(action, subject, conditions = None) -> Ability:
    return Ability(action=action, subject=subject, conditions=conditions)

def cannot(action,subject, conditions = None) -> Ability:
    return Ability(action=action, subject=subject, conditions=conditions, inverted=True)

def user_can(abilities: List[Ability], action: str, subject: str, resource: Any = None) -> bool:    
    for ability in abilities:
        # Convert to List
        actions = [ability.action] if isinstance(ability.action, str) else ability.action
        subjects = [ability.subject] if isinstance(ability.subject, str) else ability.subject
        
        if not (action in actions and (subject in subjects or 'all' in subjects)):
            continue
        
        if not ability.conditions:
            return not ability.inverted
        
        # There are conditions
        if not resource: return False
        
        if all(getattr(resource, key, None) == value for key, value in ability.conditions.items()):
            return not ability.inverted # Conditions met
    return False

#####################

async def get_user_permissions(user: User, database: Database) -> List[Ability]:
    scopes = permission_scopes(user.id)
    committee_query = (
        select(Committee)
        .join(CommitteeMember)
        .where(CommitteeMember.user_id == user.id)
    )
    committees = (await database.exec(committee_query)).all()
    role = "member"
    if any(c.name_nl == "WebCie" for c in committees):
        role = "admin"
    elif any(c.name_nl == "Bestuur" for c in committees):
        role = "board"
    elif any(c.name_nl == "Redactie" for c in committees):
        role = "contributor"

    print(f"Granted permission scope '{role}' to {user.id}")
    return scopes[role]

CREATE = "create"
EDIT = "edit"
DELETE = "delete"
APPROVE = "approve"
VIEW = "view"
VIEW_EXTENDED = "view.extended"

def permission_scopes(user_id: int):
    scopes = {}
    scopes["member"] = [
        can(EDIT, "User", {"id": user_id}),       # With restriction
        can(VIEW_EXTENDED, "User", {"id": user_id}), # With restriction
        can(VIEW_EXTENDED, "AgendaItem"),
        can(VIEW, "Subscription"),
        can([EDIT, DELETE], "Subscription", {"user_id": user_id}),
        can(VIEW, "CommitteeMember"),
        can(VIEW_EXTENDED, "NewsItem"),
        can(CREATE, VIEW, "NewsComment"),
        can([EDIT, DELETE], "NewsComment", {"user_id": user_id})
    ]

    scopes["contributor"] = \
        scopes["member"] + \
        [
            can([CREATE, EDIT, DELETE], "NewsItem"),
            can([CREATE, EDIT, DELETE], "Photo"),
            can([CREATE, EDIT, DELETE], "File")
        ]
    
    scopes["board"] = \
        scopes["contributor"] + \
        [
            can(VIEW_EXTENDED, "User"),            # Without restriction
            can([CREATE, EDIT, DELETE], "User"), 
            can(APPROVE, "NewsItem"),
            can([CREATE, EDIT, DELETE], "Committee"),
            can([CREATE, EDIT, DELETE], "CommitteeMember"),
            can([CREATE, EDIT, DELETE], "AgendaItem"),
            can([EDIT, DELETE], "Subscription"),
            can([CREATE, EDIT, DELETE], "Page"),
            can([VIEW, EDIT, DELETE], "NewsComment")
        ]

    scopes["admin"] = \
        scopes["board"] + \
        [
            can([CREATE, EDIT, DELETE, VIEW, VIEW_EXTENDED, APPROVE], 'all')
        ]
    return scopes

