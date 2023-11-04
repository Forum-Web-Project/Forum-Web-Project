from fastapi import APIRouter, Header, Query
from common.auth import get_user_or_raise_401
from services import message_service
from common.responses import NotFound, NoContent


message_router = APIRouter(prefix='/message', tags=['Messages'])


# -	Responds with a list of Messages exchanged between the authenticated user and another user
@message_router.get('/messages', description="Get all user related message by username")  # response_model=list[Message]
def get_conversation_by_username(receiver_username: str, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    if not user:
        return NotFound("Not authenticated user!")

    user_id = user.id
    result = message_service.conversation_by_username(user_id, receiver_username)

    if not result:
        return NoContent()

    return result


# - Responds with a list of all Users with which the authenticated user has exchanged messages
@message_router.get('/conversations', description="Get all related user users by id")  # response_model=list[Message]
def get_conversations(x_token: str = Header()):
    user = get_user_or_raise_401(x_token)

    if not user:
        return NotFound("Not authenticated user!")

    user_id = user.id
    messages = message_service.all_user_related_message(user_id)

    if not messages:
        return NoContent()

    return messages


@message_router.post('/')
def create_message(
        text: str = Query(),
        receiver_username: str = Query(),
        x_token: str = Header()
):

    user = get_user_or_raise_401(x_token)
    if not user:
        return NotFound("Not authenticated user!")

    name_of_receiver = message_service.check_receiver_name(receiver_username)
    sender_id = user.id

    if name_of_receiver:
        created_message = message_service.create(text, sender_id, receiver_username)

        return created_message

    return NotFound('Receiver name not exist!')
