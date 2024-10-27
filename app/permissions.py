from sqlmodel import SQLModel
from typing import Union, Optional

class Ability(SQLModel):
    action: Union[str, list[str]]
    subject: Union[str, list[str]]
    conditions: Optional[object] = None
    inverted: Optional[bool] = None

def can(action, subject, conditions = None) -> Ability:
    return Ability(action=action, subject=subject, conditions=conditions)

def cannot(action,subject, conditions = None) -> Ability:
    return Ability(action=action, subject=subject, conditions=conditions, inverted=True)
