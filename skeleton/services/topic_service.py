from data.database import read_query,insert_query
from data.models import Topic


def create_topic(title: str, text: str, users_id: int) -> Topic | None:
    # password = _hash_password(password)

        generated_id = insert_query(
            'INSERT INTO topics(title, text, users_id) VALUES (?,?,?)',
            (title, text, users_id))

        return Topic(id=generated_id, title=title, text=text, users_id=users_id)



def check_topic_exist(title:str) -> bool:

    data = read_query(
        'SELECT title FROM topics WHERE title = ?',
        (title,)
    )

    return bool(data)

