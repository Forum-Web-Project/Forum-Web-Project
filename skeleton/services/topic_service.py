from data.database import read_query,insert_query
from data.models import Topic




def check_topic_exist(title:str) -> bool:

    data = read_query(
        'SELECT title FROM topics WHERE title = ?',
        (title,)
    )

    return bool(data)



def sort(topics: list[Topic], *, attribute='users_id', reverse=False):
    if attribute == 'users_id':
        def sort_fn(t: Topic): return t.users_id
    elif attribute == 'category_id':
        def sort_fn(t: Topic): return t.category_id
    else:
        def sort_fn(t: Topic): return t.id

    return sorted(topics, key=sort_fn, reverse=reverse)


def all(search: str = None):
    if search is None:
        data = read_query(
            '''SELECT id, title, text, users_id
            FROM topics''')
    else:
        data = read_query(
            '''SELECT id, title, text, users_id
               FROM topics 
               WHERE title LIKE ?''', (f'%{search}%',))

    return (Topic.from_query_result(*row) for row in data)



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