from fastapi import APIRouter, Response, Header, HTTPException, Query, Depends
from services import category_service, topic_service, user_service
from common.responses import BadRequest, NotFound
from data.models import User
#from services.category_service import get_current_user
from fastapi.responses import JSONResponse


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
        return JSONResponse(status_code=400, content='No such category!')

    is_private = category_data[2]
    if is_private == "1":
        category_dict = {
            "id": category_data[0],
            "name": category_data[1],
            "is_private": category_data[2]
        }
    else:
        category_dict = {
            "id": category_data[0],
            "name": category_data[1],
            "is_private": category_data[2],
            "topics": topic_service.get_topics_by_category_id(category_data[0])
        }
    return category_dict


@category_router.post("/", description="Creates a category")
def create_category(
    name: str = Query(),
    is_private: bool = Query(),
    current_user_token: str = Header()
):
    category_service.check_user_role(current_user_token, "Admin")

    if not name:
        return BadRequest("Name is required!")

    if category_service.check_category_exists(name):
        return JSONResponse(status_code=400, content="Category already exists!")

    category = category_service.create_category(name, is_private)
    return category


@category_router.put("/private/{name}", description="Make Category Private / Non-private")
def make_category_private(
    name: str,
    is_private: bool = Query(),
    current_user_token: str = Header()
):
    category_service.check_user_role(current_user_token, "Admin")

    id = category_service.get_category_id_by_name(name)
    category_data = category_service.find_category_by_id(id)

    if not category_data:
        return JSONResponse(status_code=400, content='No such category!')

    category_service.update_category_privacy(id, is_private)
    # topic_service.update_topic_privacy_by_category_id(id, is_private)

    return {"message": f"Category {name} is now {'private' if is_private else 'public'}."}


@category_router.put("/{name}", description="Give Read Access to a Specific Category and Specific User")
def give_read_access_to_category(
    name: str,
    user_id: int,
    current_user_token: str = Header()
):
    category_service.check_user_role(current_user_token, "Admin")

    category_id = category_service.get_category_id_by_name(name)
    category_data = category_service.find_category_by_id(category_id)
    is_private = category_data[2]

    if not category_data:
        return JSONResponse(status_code=400, content='No such category!')

    user_data = user_service.find_user_by_id(user_id)

    if not user_data:
        return JSONResponse(status_code=400, content='No such user!')

    if is_private == "0":
        return JSONResponse(status_code=400, content='Category is not private! No need to give read access to users!')
    
    category_service.give_read_access_to_category(category_id, user_id)

    return {"message": f"User {user_data.username} now has read access to category {name}."}


# @category_router.get('/{id}', description='Get All Users That Have Read Access To A Specific Category')
# def read_access_users(id: int):
#     data = category_service.get_read_access_users(id)
#     return data[0]