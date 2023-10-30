from fastapi import HTTPException
from data.models import User
from services.user_service import from_token,is_authenticated
from fastapi import Depends
from data.models import User

def get_user_or_raise_401(token: str) -> User:
    if not is_authenticated(token):
        raise HTTPException(status_code=401)

    return from_token(token)    


# def get_current_user(token: str = Depends(get_user_or_raise_401)) -> User:
#     return token.role
