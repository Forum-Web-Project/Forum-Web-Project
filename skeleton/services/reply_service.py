from data.database import read_query,insert_query
from data.models import Reply
from services import topic_service
from fastapi import Response


def find_id_by_username(nickname):
    result = read_query(
         'SELECT id FROM users WHERE username = ?',
         (nickname,)
    )
    return result


def create_reply(text: str, username: str, topic_name: str) -> Reply| None:
    author_id = find_id_by_username(username)
    real_author_id = author_id[0][0]

    if not topic_service.check_topic_exists(topic_name):
        return Response(status_code=400, content="No such topic!")
    
    topic_id = topic_service.get_topics_id_by_title(topic_name)

    generated_id = insert_query(
        'INSERT INTO replies(text, users_id, topics_id, upvotes, downvotes) VALUES (?,?,?,?,?)',
        (text, real_author_id, topic_id, 0, 0))

    return Reply(text=text, username=username, topic_name=topic_name)


def check_reply_exists(text: str) -> bool:

        data = read_query(
            'SELECT text FROM replies WHERE text = ?',
            (text,)
        )
        return bool(data)

def get_reply_by_topic_id(topic_id: int):
     data = read_query(
          'SELECT * FROM replies WHERE topics_id = ?',
          (topic_id,)
     )
     replies = [{'text': row[1], 'users_id': row[2], 'topics_id': row[3], 'upvotes': row[4], 'downvotes': row[5]} for row in data]
     return replies