from typing import Annotated, Optional
from fastapi import APIRouter, Form, Depends, Request, Security, Query
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select, func, column
from ..authentication import *
from ..models.user import User, UserResponse
from ..dependencies import Database
from ..permissions import Ability, can, cannot
from ..config import config

router = APIRouter(prefix="/auth")

@router.post("/login") #, response_model_exclude_unset=True
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        database: Database, response: Response) -> Token:
    
    username = form_data.username
    password = form_data.password
    query = select(User) \
        .where(func.lower(column("email")) == func.lower(username))
    user = (await database.exec(query)).first()
    
    if not user:
        return Response("", 403)
    if not verify_password(password, user.encrypted_password):
        return Response("", 403)
    
    token = create_token(str(user.id))
    return Token(access_token=token, token_type="bearer")

@router.post("/logout")
async def logout():
    # requires valid session
    # remove the session from cache
    # remove the session cookie
    return Response(200)

@router.get("/current_user", response_model=UserResponse)
async def get_current_user(current_user: Annotated[Optional[User], Depends(current_user)]):
    return UserResponse.model_validate(current_user)


# maybe this belongs more to user administration than authentication?
@router.post("/register")
async def register():
    return Response(200)

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


# TODO: don't need this anymore when the JWT contains scopes
@router.get("/permissions", response_model= list[Ability], response_model_exclude_none=True)
async def permissions(request: Request, database: Database, user: Annotated[Optional[User], Depends(current_user)]):
    everyone = [can('read', 'all'),
                can(['home', 'titleshow'], 'Page'),
                can(['game'], 'Page'),
                cannot('read', 'Page'),
                can('read', 'Page', {'public':True}),
                can(['perdag', 'month'], 'Agendaitem'),
                can(['frontpage', 'records'], 'Result'),
                can(['current', 'hide'], 'Announcement'),
                can('create', ['Contact']),
                cannot('read', 'Photoalbum'),
                can('read', 'Photoalbum', {'public': True}),
                cannot('read', ['User','Photo','Announcement', 'Kronometer', 'Subscription', 'Comment']),
                can(['read','display'], 'Kronometer', {'public':True}),
                cannot('see_email', 'Commission')]

    abilities = [] + everyone

    if user is not None:
        abilities += [can('read', 'all'),
                   can('read', 'Page'),
                   can('see_email', 'Commission'),
                   can('create', ['Photo','Newsitem','Agendaitem','Event','Result','Comment']),
                   can(['archief','wedstrijden','new_result','create_result', 'icalendar', 'duplicate'], 'Agendaitem'),
                   can(['read','create','update'], 'Photoalbum'),
                   can(['create', 'update'], ['Subscription'], {'user_id': user.id}),
                   can('display', 'Kronometer'),
                   can('update', 'Agendaitem', {'user_id': user.id}),
                   can(['update','editpassword'], 'User', {'id':user.id}),
                   can('birthdays', 'User'),
                   cannot('create', 'User')]

        abilities += [can('destroy', 'Subscription', {'id':sub.id}) for sub in user.subscriptions if sub.agendaitem.is_before_deadline()]
        
        if len(user.commission_memberships) > 0:
            abilities += [can('manage', 'Agendaitem', {'user_id': user.id})]           
            abilities += [can('update', 'Agendaitem', {'commission_id': cm.commission_id}) for cm in user.commission_memberships]
            
            for cm in user.commission_memberships:
                match cm.commission.role:
                    case "KRONOMETER_ADMIN":
                        abilities += [can('kronometer_list', 'User'),
                         can('manage', 'Kronometer')]
                    case "RESULT_ADMIN":
                        abilities += [can('manage', 'Result')]
                    case "ADMIN":
                        abilities += [can('manage', 'all'),
                                      can(['update_mailinglists', 'update_announcements'], 'User'),
                                      cannot('destroy', 'User')]
            
    
    return abilities
