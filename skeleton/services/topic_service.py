from data.database import read_query,insert_query
from data.models import Topic
from services import category_service




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
            '''SELECT id, title, text, users_id, categories_id
            FROM topics''')
    else:
        data = read_query(
            '''SELECT id, title, text, users_id, categories_id
               FROM topics 
               WHERE title LIKE ?''', (f'%{search}%',))

    return (Topic.from_query_result(*row) for row in data)

def find_id_by_username(nickname):
    result = read_query(
         'SELECT id FROM users WHERE username = ?',
         (nickname,)
    )
    return result

def check_topic_exists(title: str) -> bool:

        data = read_query(
            'SELECT title FROM topics WHERE title = ?',
            (title,)
        )
        return bool(data)

def create_topic(title: str, text: str, username: str, category_id: int) -> Topic| None:
    # password = _hash_password(password)
    author_id = find_id_by_username(username)
    real_author_id = author_id[0][0]
    category_does_exist = ""
    # # found_category = category_view_service.check_category_exists(category_name)
    if category_service.check_category_exists(category_id):
        category_does_exist = category_id
    generated_id = insert_query(
    'INSERT INTO topics(title, text, users_id, up_vote, down_vote, categories_id) VALUES (?,?,?,?,?,?)',
    (title, text, real_author_id, 0, 0, category_id))

    return Topic(title=title, text=text, username=username, category_id=category_does_exist)


def get_by_id(id: int):
    data = read_query(
        '''SELECT id, title, text, users_id, categories_id
            FROM topics 
            WHERE id = ?''', (id,))

    return next((Topic.from_query_result(*row) for row in data), None)