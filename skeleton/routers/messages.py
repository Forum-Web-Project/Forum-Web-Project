from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from common.auth import get_user_or_raise_401
from services import message_service, user_service
from data.models import Message, User
from common.responses import NotFound, Unauthorized
from services.message_service import check_receiver_name, conversation_by_username
from services.user_service import find_by_username, check_username_exist


message_router = APIRouter(prefix='/message')


@message_router.get('/{id}', response_model=list[Message])
def get_conversations(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if not user:
        return NotFound()

    messages = message_service.all_user_related_message(id)

    return messages


@message_router.get('/{name}', tags=["Receiver username"], response_model=list[Message])
def get_conversation_by_username(name: str, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if not user:
        return NotFound("Not authenticated user!")

    result = conversation_by_username(name)

    if not result:
        return NotFound('No message found!')

    return result


@message_router.post('/', tags=["Create message"])
def create_message(message: Message, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    name_of_receiver = check_receiver_name(message.receiver_username)

    if name_of_receiver:
        created_message = message_service.create(message)

        return created_message

    return NotFound('Receiver name not exist!')


