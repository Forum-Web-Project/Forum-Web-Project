from fastapi import APIRouter, Response, Header, HTTPException, Query
from services import category_service, topic_service
from common.responses import BadRequest, NotFound


category_router = APIRouter(prefix='/category', tags=['Categories'])


@category_router.get('/', description="Get All Categories (Sorting name by ascending and descending [asc/desc])")
def get_categories(
    sort: str = Query(default="asc"),
    search: str | None = None
):
    if search:
        categories = category_service.get_categories_by_name(search)
    elif sort:
        categories = category_service.sort_categories(sort)
    else:
        categories = category_service.read_categories()

    result = []

    for data in categories:
        category_dict = {
            "id": data[0],
            "name": data[1],
            "is_private": data[2],
        }
        result.append(category_dict)
    return result


@category_router.get('/{name}', description="Get Category By Name And All Of Its Topics")
def get_category_by_name(name: str):
    id = category_service.get_category_id_by_name(name)
    category_data = category_service.find_category_by_id(id)

    if not category_data:
        return Response(status_code=400, content='No such category!')

    category_dict = {
            "id": category_data[0],
            "name": category_data[1],
            "is_private": category_data[2],
            "topics": topic_service.get_topics_by_category_id(category_data[0])
        }
    return category_dict