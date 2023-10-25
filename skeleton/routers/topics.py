from fastapi import APIRouter, Response, Header, HTTPException, Query
from services import user_service, topic_service
from data.models import Topic
from common.responses import BadRequest, NotFound
from common.auth import get_user_or_raise_401


topics_router = APIRouter(prefix='/topic')


@topics_router.get('/', response_model=list[Topic])
def get_topics(
    sort: str | None = None,
    sort_by: str | None = None,
    search: str | None = None
):
    result = topic_service.all(search)

    if sort and (sort == 'asc' or sort == 'desc'):
        return topic_service.sort(result, reverse=sort == 'desc', attribute=sort_by)
    else:
        return result


@topics_router.get('/{id}')
def get_topic_by_id(id: int):
    topic = topic_service.get_by_id(id)

    if topic is None:
        return NotFound()
    else:
        return topic
    

@topics_router.post("/create_topic", tags=["Create Topic"])
def create_topic(x_token: str = Header(),
                title: str  = Query(), 
                text: str = Query(),
                username: str = Query(),
                category_id: int = Query()
            ):
    user = get_user_or_raise_401(x_token)

    if topic_service.check_topic_exists(title):
        return Response(status_code=400, content=f'Topic with such title already exists!')
    else:
        result = topic_service.create_topic(title, text, username, category_id)
        return result