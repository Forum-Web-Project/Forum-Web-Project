from fastapi import APIRouter, Response, Header, HTTPException, Query
from services import user_service, topic_service, category_service, reply_service
from data.models import Topic
from common.responses import BadRequest, NotFound
from common.auth import get_user_or_raise_401


topics_router = APIRouter(prefix='/topic', tags=['Topic'])


@topics_router.get('/', description='Get All Topics (Sorting works with IDs - lowest or highest)')
def get_topics(
    sort: str = Query(default="lowest"),
    search: str | None = None
):
    if search:
        topics = topic_service.get_topics_by_title(search)
    elif sort:
        topics = topic_service.sort_topics(sort)
    else:
        topics = topic_service.read_topics()

    result = []
    for data in topics:
        topic_dict = {
            "id": data[0],
            "title": data[1],
            "text": data[2],
            "username": user_service.find_username_by_id(data[3]),
            "up_vote": data[4],
            "down_vote": data[5],
            "category_name": category_service.get_category_name_by_id(data[6])
        }
        result.append(topic_dict)
    return result


@topics_router.get('/{id}', description="Get topic by ID")
def get_topic_by_id(id: int):
    topic_data = topic_service.find_topic_by_id(id)

    if not topic_data:
        return Response(status_code=400, content='No such topic!')

    topic_dict = {
            "id": topic_data[0],
            "title": topic_data[1],
            "text": topic_data[2],
            "username": user_service.find_username_by_id(topic_data[3]),
            "up_vote": topic_data[4],
            "down_vote": topic_data[5],
            "category_name": category_service.get_category_name_by_id(topic_data[6]),
            "replies": reply_service.get_reply_by_topic_id(topic_data[0])
        }
    return topic_dict
    

@topics_router.post("/", description="Creates a topic")
def create_topic(x_token: str = Header(),
                title: str  = Query(), 
                text: str = Query(),
                category_name: str = Query()
            ):
    user = get_user_or_raise_401(x_token)
    username = user_service.get_nickname_from_token(x_token)
    category_id = category_service.get_category_id_by_name(category_name)

    if topic_service.check_topic_exists(title):
        return Response(status_code=400, content=f'Topic with such title already exists!')
    else:
        result = topic_service.create_topic(title, text, username, category_id)
        return result