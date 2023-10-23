from fastapi import APIRouter, Response, Header, HTTPException
from services import user_service
from data.models import Topic


topics_router = APIRouter(prefix='/topic')


@topics_router.post('/', tags=["Create topic"])
def create_topic(data: Topic, token: str = Header()):
    if user_service.is_authenticated(token):

        if user_service.check_topic_exist(data.title):
            return Response(status_code=400, content=f'Topic with this name exist!')
        else:
            topic = user_service.create_topic(data.title, data.text, data.users_id)
            return topic
    else:
        raise HTTPException(status_code=401)