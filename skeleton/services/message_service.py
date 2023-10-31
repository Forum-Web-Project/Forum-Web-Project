from data.database import read_query, insert_query
from data.models import Message


def all_user_related_message(id: int):
    data = read_query(
        '''SELECT id, text, sender_id, receiver_username FROM messages WHERE sender_id = ?''',
        (id,))

    if not data:
        return None

    return (Message.from_query_result(*row) for row in data)


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

