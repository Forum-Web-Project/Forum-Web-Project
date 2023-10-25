from fastapi import APIRouter, Response, Header, HTTPException
from services import category_service
from data.models import Category
from common.responses import BadRequest, NotFound


category_router = APIRouter(prefix='/category')


@category_router.get('/', response_model=list[Category])
def get_categories(
    sort: str | None = None,
    search: str | None = None
):
    result = category_service.all(search)

    if sort and (sort == 'asc' or sort == 'desc'):
        return category_service.sort(result, reverse=sort == 'desc')
    else:
        return result
