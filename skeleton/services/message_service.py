from data.database import read_query, insert_query
from data.models import Message
from services import user_service


def all():
    data = read_query(
        '''SELECT id, text, user_id, receiver_username 
            FROM messages''')

    return (Message.from_query_result(*row) for row in data)


def get_conversation_by_user_id():
    pass

from data.database import read_query, insert_query
from data.models import Message
from services import user_service


def all_user_related_message(id: int):
    # data = read_query(
    #     '''SELECT id, text, sender_id, receiver_username FROM messages WHERE sender_id = ?''',
    #     (id,))
    #
    # if not data:
    #     return None
    #
    # return (Message.from_query_result(*row) for row in data)

    # The method above return id, text, sender_id, receiver_username

    data = read_query(
        '''SELECT receiver_username FROM messages WHERE sender_id = ?''',
        (id,))

    if not data:
        return None

    return next((Message(receiver_username=receiver_username) for receiver_username in data), None)


def conversation_by_username(name: str = None):

    data = read_query(
        '''SELECT id, text, sender_id, receiver_username
           FROM messages 
           WHERE receiver_username LIKE ?''', (name,))

    return (Message.from_query_result(*row) for row in data)


def create(message: Message) -> Message | None:

    generated_id = insert_query(
        '''INSERT INTO messages(id, text, sender_id, receiver_username) VALUES (?,?,?,?)''',
        (message.id, message.text, message.sender_id, message.receiver_username))

    message.id = generated_id

    return message


def check_receiver_name(receiver_username: str) -> bool:
    data = read_query(
        '''SELECT username FROM users WHERE username = ?''',
        (receiver_username,)
    )

    result = data

    return bool(result)


def create(message: Message) -> Message | None:

    generated_id = insert_query(
        '''INSERT INTO messages(id, text, sender_id, receiver_username) VALUES (?,?,?,?)''',
        (message.id, message.text, message.sender_id, message.receiver_username))

    message.id = generated_id

    return message


def check_receiver_name(receiver_username: str) -> bool:
    data = read_query(
        '''SELECT username FROM users WHERE username = ?''',
        (receiver_username,)
    )

    result = data

    return bool(result)
