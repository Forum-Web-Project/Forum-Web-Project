from fastapi import APIRouter, Header, HTTPException
from common.auth import get_user_or_raise_401
from services import message_service
from data.models import Message, User
from common.responses import NotFound, Unauthorized
from services.user_service import find_by_username


message_router = APIRouter(prefix='/message')


@message_router.get('/', response_model=list[Message])
def get_conversations(token: str = Header()):
    user = get_user_or_raise_401(token)

    if not user:
        return Unauthorized('Not authenticated user!')

    messages = message_service.all()

    return messages


@message_router.get('/{username}')
def get_conversation_by_username():
    pass


@message_router.post('/', tags=["Create message"])
def create_message(message: Message, x_token: str = Header()):

    user = get_user_or_raise_401(x_token)

    name_of_receiver = find_by_username(message.receiver_username)

    if name_of_receiver:
        result = message_service.create(message)

        return result

    return NotFound('Receiver name not exist!')
