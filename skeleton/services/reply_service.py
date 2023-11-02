from data.database import read_query,insert_query,update_query
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

def read_replies():
    data = read_query('SELECT * FROM replies')
    return data

def check_if_already_upvoted(users_id, reply_id):
     data = read_query(
          "SELECT users_id, replies_id FROM reactions WHERE users_id = ? AND replies_id = ? and reaction = ?",
          (users_id, reply_id, 1)
     )
     return bool(data)

def check_if_already_downvoted(users_id, reply_id):
     data = read_query(
          "SELECT users_id, replies_id FROM reactions WHERE users_id = ? AND replies_id = ? and reaction = ?",
          (users_id, reply_id, 0)
     )
     return bool(data)

def remove_downvote_from_reply(reply_id: int):
     data = update_query(
          "UPDATE replies SET downvotes = downvotes - 1 WHERE id = ?",
          (reply_id,)
     )
     return data

def set_reaction_to_one(users_id, reply_id):
     data = update_query(
          "UPDATE reactions SET reaction = 1 WHERE users_id = ? and replies_id = ? and reaction = ?",
          (users_id, reply_id, 0)
     )
     return data

def upvote_reply(reply_id: int):
     data = update_query(
          "UPDATE replies SET upvotes = upvotes + 1 WHERE id = ?",
          (reply_id,)
     )
     return data

def check_reply_exists_by_id(id: int) -> bool:

        data = read_query(
            'SELECT id FROM replies WHERE id = ?',
            (id,)
        )
        return bool(data)

def add_upvote_to_reactions(user_id, reply_id):
    data = insert_query(
         "INSERT INTO reactions(users_id, replies_id, reaction) VALUES(?,?,?)",
         (user_id, reply_id, 1,)
    )
    return data

def remove_upvote_from_reply(reply_id: int):
     data = update_query(
          "UPDATE replies SET upvotes = upvotes - 1 WHERE id = ?",
          (reply_id,)
     )
     return data

def set_reaction_to_zero(users_id, reply_id):
     data = update_query(
          "UPDATE reactions SET reaction = 0 WHERE users_id = ? and replies_id = ? and reaction = ?",
          (users_id, reply_id, 1)
     )
     return data

def downvote_reply(reply_id: int):
     data = update_query(
          "UPDATE replies SET downvotes = downvotes + 1 WHERE id = ?",
          (reply_id,)
     )
     return data

def add_downvote_to_reactions(user_id, reply_id):
    data = insert_query(
         "INSERT INTO reactions(users_id, replies_id, reaction) VALUES(?,?,?)",
         (user_id, reply_id, 0,)
    )
    return data