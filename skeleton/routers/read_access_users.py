from fastapi import APIRouter
from services import category_service

user_router = APIRouter(prefix='/categori', tags=['Categories'])


@user_router.get('/{id}', description='Get All Users That Have Read Access To A Specific Category')
def read_access_users(id: int):
    data = category_service.get_read_access_users(id)
    return data[0]