from data.database import read_query,insert_query,update_query
from data.models import Topic
from services import category_service
from fastapi import Response
from fastapi.responses import JSONResponse


def check_topic_exist(title:str) -> bool:

    data = read_query(
        'SELECT title FROM topics WHERE title = ?',
        (title,)
    )

    return bool(data)


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
    author_id = find_id_by_username(username)
    real_author_id = author_id[0][0]

    if not category_service.check_category_exists_for_topic(category_id):
        return JSONResponse(status_code=400, content="No such category!")

    generated_id = insert_query(
        'INSERT INTO topics(title, text, users_id, up_vote, down_vote, categories_id) VALUES (?,?,?,?,?,?)',
        (title, text, real_author_id, 0, 0, category_id))

    return Topic(title=title, text=text, username=username, category_id=category_id)


def get_by_id(id: int):
    data = read_query(
        '''SELECT id, title, text, users_id, categories_id
            FROM topics 
            WHERE id = ?''', (id,))

    return next((Topic.from_query_result(*row) for row in data), None)


def find_topic_by_id(id: int):
    data = read_query(
        "SELECT * FROM topics WHERE id = ?",
        (id,)
    )
    if data:
        return data[0]
    else:
        return None


def read_topics():
    data = read_query('SELECT * FROM topics')
    return data


def get_topics_by_title(title_search: str):
    data = read_query(
        'SELECT * FROM topics WHERE title LIKE ?',
        (f"%{title_search}%",)
    )

    return data


def sort_topics(requirement: str):
    order_by = ''
    if requirement == "lowest":
        order_by = 'id ASC'
    elif requirement == "highest":
        order_by = 'id DESC'

    data = read_query(f'SELECT * FROM topics ORDER BY {order_by}')

    return data


def get_topics_by_category_id(id: int):
    data = read_query(
        "SELECT * FROM topics WHERE categories_id = ?",
        (id,)
    )
    topics = [{'title': row[1], 'text': row[2], 'users_id': row[3], 'up_vote': row[4], 'down_vote': row[5], 'categories_id': row[6]} for row in data]
    return {"category": category_service.get_category_name_by_id(id), "topics": topics}

def get_topics_id_by_title(title_search: str):
    data = read_query(
        'SELECT id FROM topics WHERE title LIKE ?',
        (f"%{title_search}%",)
    )
    return data[0][0]

def check_if_user_is_owner(logged_user_id: int, topic_id: int):
    check = read_query('SELECT * FROM topics WHERE id = ? AND users_id = ?', (topic_id, logged_user_id))
    return bool(check)

def choose_best_reply(reply_id,topic_id):
    check = read_query(
        "SELECT * FROM replies WHERE topics_id = ?",
        (topic_id,)
    )
    if check:
        update = update_query('UPDATE replies SET is_best_reply = 1 WHERE id = ? AND topics_id = ?', (reply_id, topic_id))
        update_query('UPDATE replies SET is_best_reply = 0 WHERE id != ? AND topics_id = ?', (reply_id,topic_id))
        return JSONResponse(status_code=200, content=f'Updated best reply for topic {topic_id}!')
    else:
        return JSONResponse(status_code=400, content="This reply does not belong to this topic!")