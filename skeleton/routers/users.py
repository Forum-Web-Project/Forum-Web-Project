from fastapi import APIRouter, Response, Query
from services import user_service


users_router = APIRouter(prefix='/users')


@users_router.post('/login', tags=["Login"])
def login(username: str = Query(), password: str = Query()):
    user = user_service.try_login(username, password)

    if user:
        token = user_service.create_token(user)
        return {'token': token}
    else:
        return Response(status_code=404, content='Invalid login data')


@users_router.post('/register', tags=["Signup"])
def register(username: str = Query(),
             password: str = Query(),
             email: str = Query(),
             # role: str = Query(default="User")
             ):
    # if role not in ["User", "Admin"]:
    #     return Response(status_code=400, content=f'Invalid role!')

    if user_service.check_username_exist(username):
        return Response(status_code=400, content=f'Username is already taken!')
    else:
        user = user_service.create_user(username, password, email)
        return user
