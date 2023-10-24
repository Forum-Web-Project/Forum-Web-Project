from fastapi import APIRouter, Response, Header, HTTPException
from services import user_service, topic_service
from data.models import Topic
from common.responses import BadRequest, NotFound


topics_router = APIRouter(prefix='/topic')


@topics_router.post('/', tags=["Create topic"])
def create_topic(data: Topic, token: str = Header()):
    if user_service.is_authenticated(token):

        if topic_service.check_topic_exist(data.title):
            return Response(status_code=400, content=f'Topic with this name exist!')
        else:
            topic = topic_service.create_topic(data.title, data.text, data.users_id)
            return topic
    else:
        raise HTTPException(status_code=401)
    

@topics_router.get('/{id}')
def get_topic_by_id(id: int):
    topic = topic_service.get_by_id(id)

    if topic is None:
        return NotFound()
    else:
        return topic