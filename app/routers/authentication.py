from typing import Annotated
from fastapi import APIRouter, Form, Depends, Request, Query
from fastapi.responses import Response
from sqlmodel import select, func, column
from ..authentication import *
from ..models.user import User, UserResponse
from ..dependencies import Database, ActiveUser
from ..permissions import Ability, can, cannot
from ..config import config

router = APIRouter(prefix="/auth")

@router.post("/login", response_model=UserResponse) #, response_model_exclude_unset=True
async def login(username: Annotated[str, Form()] , password:Annotated[str, Form()], database: Database, response: Response):
    query = select(User) \
        .where(func.lower(column("email")) == func.lower(username))
    
    user = (await database.exec(query)).first()

    if not user:
        return Response("", 403)
    if not verify_password(password, user.encrypted_password):
        return Response("", 403)

    token = create_token(str(user.id))

    if token is None:
        # log login result
        return Response("", 403)
    else:
        # log login result
        #response.set_cookie(key="v2-access-token", value=token, max_age=3600*24*30, secure=True, httponly=True,)
        response.headers["access-token"] = token
        user = await database.get(User, user.id)
        return UserResponse.model_validate(user, update={})

@router.post("/logout")
async def logout():
    # requires valid session
    # remove the session from cache
    # remove the session cookie
    return Response(200)


# class JWTMiddleware that will renew an access token / set a session token

class PermissionCheck:
    def __init__(self, required_scopes: [str]):
        self.required_scopes = required_scopes
    async def __call__(self, request: Request):
        data = request.cookies["v2-access-token"]
        token = await validate_token(data)
        user_scopes = token["scopes"]

        check = all(s in user_scopes for s in self.required_scopes)
        print(check, user_scopes, self.required_scopes)
        
        
@router.get("/scope")
async def validate_scope(user: Annotated[str, Depends(PermissionCheck(config['permissions']['scopes']['test']))]):
    return Response("",200)

@router.get("/validate_token",response_model=UserResponse)
async def validate(request: Request, database: Database, token: Annotated[str | None, Query(alias="access-token")] = None,  ):
    #token = request.cookies["v2-access-token"]
    payload = await validate_token(token)
    user_id: str = payload.get("sub")
    user = await database.get(User, int(user_id))
    return UserResponse.model_validate(user, update={'id':user_id})


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

@router.get("/permissions", response_model= list[Ability], response_model_exclude_none=True)
async def permissions(request: Request, database: Database, active_user: ActiveUser):
    
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
    
    if active_user is not None:
        abilities += [can('read', 'all'),
                   can('read', 'Page'),
                   can('see_email', 'Commission'),
                   can('create', ['Photo','Newsitem','Agendaitem','Event','Result','Comment']),
                   can(['archief','wedstrijden','new_result','create_result', 'icalendar', 'duplicate'], 'Agendaitem'),
                   can(['read','create','update'], 'Photoalbum'),
                   can(['create', 'update'], ['Subscription'], {'user_id': active_user.id}),
                   can('display', 'Kronometer'),
                   can('update', 'Agendaitem', {'user_id': active_user.id}),
                   can(['update','editpassword'], 'User', {'id':active_user.id}),
                   can('birthdays', 'User'),
                   cannot('create', 'User')]

        abilities += [can('destroy', 'Subscription', {'id':sub.id}) for sub in active_user.subscriptions if sub.agendaitem.is_before_deadline()]
        
        if len(active_user.commission_memberships) > 0:
            abilities += [can('manage', 'Agendaitem', {'user_id': active_user.id})]           
            abilities += [can('update', 'Agendaitem', {'commission_id': cm.commission_id}) for cm in active_user.commission_memberships]
            
            for cm in active_user.commission_memberships:
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
