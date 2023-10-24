from data.database import read_query,insert_query
from data.models import Topic




def check_topic_exist(title:str) -> bool:

    data = read_query(
        'SELECT title FROM topics WHERE title = ?',
        (title,)
    )

    return bool(data)


def create_topic(title: str, text: str, users_id: int) -> Topic | None:
    # password = _hash_password(password)

        generated_id = insert_query(
            'INSERT INTO topics(title, text, users_id) VALUES (?,?,?)',
            (title, text, users_id))

        return Topic(id=generated_id, title=title, text=text, users_id=users_id)


def get_by_id(id: int):
    data = read_query(
        '''SELECT id, title, text, users_id
            FROM topics 
            WHERE id = ?''', (id,))

    return next((Topic.from_query_result(*row) for row in data), None)