from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from common.auth import get_user_or_raise_401
from services import message_service
from data.models import Message, User
from common.responses import NotFound, Unauthorized


message_router = APIRouter(prefix='/message', tags=['Messages'])


# - Responds with a list of all Users with which the authenticated user has exchanged messages
@message_router.get('/{id}', description="Get all related user users by id", response_model=list[Message])
def get_conversations(id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if not user:
        return NotFound()

    messages = message_service.all_user_related_message(id)

    return messages


# -	Responds with a list of Messages exchanged between the authenticated user and another user
@message_router.get('/{name}', description="Get all user related message by username", response_model=list[Message])
def get_conversation_by_username(name: str, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    if not user:
        return NotFound("Not authenticated user!")

    result = message_service.conversation_by_username(name)

    if not result:
        return NotFound('No message found!')

    return result


@message_router.post('/',)
def create_message(message: Message, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    name_of_receiver = message_service.check_receiver_name(message.receiver_username)

    if name_of_receiver:
        created_message = message_service.create(message)

        return created_message

    return NotFound('Receiver name not exist!')


