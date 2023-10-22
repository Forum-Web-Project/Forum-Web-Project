from fastapi import APIRouter, Response, Query
from skeleton.services import user_service
from datetime import date



users_router = APIRouter(prefix='/users')


@users_router.post('/login', tags=["Signup"])
def login(username: str = Query(),password: str = Query()):
    user = user_service.try_login(username, password)

    if user:
        token = user_service.create_token(user)
        return {'token': token}
    else:
        return Response(status_code=404, content='Invalid login data')


@users_router.post('/register', tags=["Signup"])
def register(email: str  = Query(), 
             username: str = Query(), 
             password: str = Query(), 
             date_of_birth: date = Query(), 
             gender: str = Query()):

    if user_service.check_email_exist(email):
        return Response(status_code=400, content=f'Email is already taken!')

    if user_service.check_username_exist(username):
        return Response(status_code=400, content=f'Username is already taken!')
    else:
        user = user_service.create_user(email, username, password,date_of_birth,gender)
        return user