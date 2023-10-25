from fastapi import APIRouter, Response, Header, HTTPException
from services import category_service
from data.models import AllCategories
from common.responses import BadRequest, NotFound


category_router = APIRouter(prefix='/category')


@category_router.get('/', response_model=list[AllCategories])
def get_categories(
    sort: str | None = None,
    search: str | None = None
):
    result = category_service.all(search)

    if sort and (sort == 'asc' or sort == 'desc'):
        return category_service.sort(result, reverse=sort == 'desc')
    else:
        return result



@category_router.get('/{id}')
def get_category_by_id(id: int):
    category = category_service.get_by_id(id)

    if category is None:
        return NotFound()
    else:
        return category