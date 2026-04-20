from typing import Annotated, Optional
from fastapi import APIRouter, Form, Depends, Request, Security, Query
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select, func, column
from ..authentication import *
from ..models.committees import Committee, CommitteeMember
from ..models.user import *
from ..dependencies import Database
from ..permissions import *
from ..config import config
from ..time_utils import now

router = APIRouter(prefix="/auth")

@router.post("/login", response_model=Token) #, response_model_exclude_unset=True
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        database: Database, response: Response) -> Token:
    
    username = form_data.username
    password = form_data.password
    query = select(User) \
        .where(func.lower(column("email")) == func.lower(username))
    user = (await database.exec(query)).first()
    
    if not user:
        return Response("Invalid username", 403)
    if not verify_password(password, user.password):
        return Response("Invalid password", 403)
    
    token = create_token(user)
    return Token(access_token=token, token_type="bearer")

@router.post("/logout")
async def logout():
    # Backend is stateless, so logging out is primarily a frontend action
    # => No need for calling this endpoint
    return {"detail": "Successfully logged out"}

@router.get("/current_user", response_model=UserExtendedResponse)
async def get_current_user(current_user: Annotated[Optional[User], Depends(get_current_user)]):
    return UserExtendedResponse.model_validate(current_user)


# maybe this belongs more to user administration than authentication?
@router.post("/register", response_model=User)
async def register(user_data: UserCreate, database: Database):
    t = now()
    hashed_password = hash_password(user_data.password)
    user = User.model_validate(user_data, update={'created_at': t, 'updated_at': t, 'password': hashed_password})
    database.add(user)
    await database.commit()
    await database.refresh(user)
    return user

# TODO: Implement
@router.post("/forgot-password")
async def forgot_password():
    # generate temporary login token (validity xx hours)
    # add field {can_reset_password: true}
    # lookup user in db if last_reset is more than some time ago: set it to now() and return succes,
    # send email
    # 
    return Response(200)


@router.post("/reset-password")
async def reset_password():
    # requires valid token that  has {can_reset_password:true }
    return Response(200)

@router.get("/permissions", response_model=List[Ability])
async def get_permissions(r: Request, database: Database, user: Annotated[User, Depends(get_current_user)]):
    scopes = permission_scopes(user.id)

    committee_query = (
        select(Committee)
        .join(CommitteeMember)
        .where(CommitteeMember.user_id == user.id)
    )
    committees = (await Database.exec(committee_query)).all()
    role = "member"
    if any(c.name_nl == "Redactie" for c in committees):
        role = "redactie"
    if any(c.name_nl == "Bestuur" for c in committees):
        role = "board"
    if any(c.name_nl == "WebCie" for c in committees):
        role = "admin"
    return scopes[role]


# OLD CODE:
# @router.get("/permissions", response_model= list[Ability], response_model_exclude_none=True)
# async def permissions(request: Request, database: Database, user: Annotated[Optional[User], Depends(current_user)]):
#     everyone = [can('read', 'all'),
#                 can(['home', 'titleshow'], 'Page'),
#                 can(['game'], 'Page'),
#                 cannot('read', 'Page'),
#                 can('read', 'Page', {'public':True}),
#                 can(['perdag', 'month'], 'Agendaitem'),
#                 can(['frontpage', 'records'], 'Result'),
#                 can(['current', 'hide'], 'Announcement'),
#                 can('create', ['Contact']),
#                 cannot('read', 'Photoalbum'),
#                 can('read', 'Photoalbum', {'public': True}),
#                 cannot('read', ['User','Photo','Announcement', 'Kronometer', 'Subscription', 'Comment']),
#                 can(['read','display'], 'Kronometer', {'public':True}),
#                 cannot('see_email', 'Committee')]

#     abilities = [] + everyone

#     if user is not None:
#         abilities += [can('read', 'all'),
#                    can('read', 'Page'),
#                    can('see_email', 'Committee'),
#                    can('create', ['Photo','Newsitem','Agendaitem','Event','Result','Comment']),
#                    can(['archief','wedstrijden','new_result','create_result', 'icalendar', 'duplicate'], 'Agendaitem'),
#                    can(['read','create','update'], 'Photoalbum'),
#                    can(['create', 'update'], ['Subscription'], {'user_id': user.id}),
#                    can('display', 'Kronometer'),
#                    can('update', 'Agendaitem', {'user_id': user.id}),
#                    can(['update','editpassword'], 'User', {'id':user.id}),
#                    can('birthdays', 'User'),
#                    cannot('create', 'User')]

#         abilities += [can('destroy', 'Subscription', {'id':sub.id}) for sub in user.subscriptions if sub.agendaitem.is_before_deadline()]
        
#         if len(user.Committee_memberships) > 0:
#             abilities += [can('manage', 'Agendaitem', {'user_id': user.id})]           
#             abilities += [can('update', 'Agendaitem', {'Committee_id': cm.Committee_id}) for cm in user.Committee_memberships]
            
#             for cm in user.Committee_memberships:
#                 match cm.Committee.role:
#                     case "KRONOMETER_ADMIN":
#                         abilities += [can('kronometer_list', 'User'),
#                          can('manage', 'Kronometer')]
#                     case "RESULT_ADMIN":
#                         abilities += [can('manage', 'Result')]
#                     case "ADMIN":
#                         abilities += [can('manage', 'all'),
#                                       can(['update_mailinglists', 'update_announcements'], 'User'),
#                                       cannot('destroy', 'User')]
            
    
#     return abilities
