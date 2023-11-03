from data.database import read_query, insert_query
from data.models import Message


def conversation_by_username(sender_id: int, receiver_username: str = None):

    data = read_query(
        '''SELECT text FROM messages 
            WHERE sender_id = ? AND receiver_username LIKE ?''',
        (sender_id, receiver_username))

    messages = [row[0] for row in data if row[0]]

    return messages


def all_user_related_message(id: int):
    data = read_query(
        '''SELECT DISTINCT receiver_username 
            FROM messages 
            WHERE sender_id = ?''',
        (id,))

    usernames = [row[0] for row in data if row[0]]

    return usernames


def create(text: str, sender_id: int, receiver_username: str) -> Message | None:
    generated_id = insert_query(
        '''INSERT INTO messages(text, sender_id, receiver_username) 
            VALUES (?,?,?)''',
        (text, sender_id, receiver_username))

    return Message(id=generated_id, text=text, sender_id=sender_id, receiver_username=receiver_username)


def check_receiver_name(receiver_username: str) -> bool:
    data = read_query(
        '''SELECT username 
            FROM users 
            WHERE username = ?''',
        (receiver_username,))

    result = data

    return bool(result)
