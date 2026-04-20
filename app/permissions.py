from sqlmodel import SQLModel
from typing import Union, Optional, Any
from .models import User

class Ability(SQLModel):
    action: Union[str, list[str]]
    subject: Union[str, list[str]]
    conditions: Optional[object] = None
    inverted: Optional[bool] = None

def can(action, subject, conditions = None) -> Ability:
    return Ability(action=action, subject=subject, conditions=conditions)

def cannot(action,subject, conditions = None) -> Ability:
    return Ability(action=action, subject=subject, conditions=conditions, inverted=True)

def user_can(user: Optional[User], action: str, subject: str, resource: Any = None) -> bool:
    if not user:
        return False
    
    abilities = permission_scopes(user.id)
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

CREATE = "create"
EDIT = "edit"
DELETE = "delete"
APPROVE = "approve"
VIEW = "view"
VIEW_EXTENDED = "view.extended"

def permission_scopes(user_id: int):
    scopes = []
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
        scopes["user"] + \
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
            can([CREATE, EDIT, DELETE]),
            can([EDIT, DELETE], "Subscription"),
            can([CREATE, EDIT, DELETE], "Page"),
            can([VIEW, EDIT, DELETE], "NewsComment")
        ]

    scopes["admin"] = \
        scopes["board"] + \
        [
            can([CREATE, EDIT, DELETE, VIEW_EXTENDED], 'all')
        ]
    return scopes

