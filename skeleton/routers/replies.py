from fastapi import APIRouter, Response, Header, HTTPException, Query
from services import user_service, topic_service, category_service, reply_service
from common.auth import get_user_or_raise_401

reply_router = APIRouter(prefix='/reply', tags=['Replies'])

@reply_router.post("/create_reply")
def create_reply(x_token: str = Header(),
                text: str  = Query(), 
                topic_name: str = Query(),
            ):
    user = get_user_or_raise_401(x_token)
    username = user_service.get_nickname_from_token(x_token)

    if reply_service.check_reply_exists(text):
        return Response(status_code=400, content=f'Such reply already exists!')
    else:
        result = reply_service.create_reply(text, username, topic_name)
        return result