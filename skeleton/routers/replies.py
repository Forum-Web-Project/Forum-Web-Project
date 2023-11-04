from fastapi import APIRouter, Response, Header, HTTPException, Query
from services import user_service, topic_service, category_service, reply_service
from common.auth import get_user_or_raise_401
from fastapi.responses import JSONResponse

reply_router = APIRouter(prefix='/reply', tags=['Replies'])

_SEPARATOR = ';'

@reply_router.get('/', description='Get All Replies')
def get_replies():
    replies = reply_service.read_replies()

    result = []
    for data in replies:
        reply_dict = {
            "id": data[0],
            "text": data[1],
            "users_id": data[2],
            "topics_id": data[3],
            "upvotes": data[4],
            "downvotes": data[5]
        }
        result.append(reply_dict)
    return result


@reply_router.post("/", description="Creates a reply for a certain topic")
def create_reply(x_token: str = Header(),
                text: str  = Query(), 
                topic_name: str = Query(),
            ):
    user = get_user_or_raise_401(x_token)
    username = user_service.get_nickname_from_token(x_token)
    is_best_reply = False

    if reply_service.check_reply_exists(text):
        return Response(status_code=400, content=f'Such reply already exists!')
    else:
        result = reply_service.create_reply(text, username, topic_name, is_best_reply)
        return result



@reply_router.put("/{reply_id}/upvote", description="Upvote a reply")
def upvote_reply(reply_id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    user_id, _ = x_token.split(_SEPARATOR)

    if reply_service.check_if_already_upvoted(user_id, reply_id):
        return JSONResponse(status_code=400, content=f'You already upvoted this reply!')
    
    if reply_service.check_if_already_downvoted(user_id, reply_id):
        reply_service.remove_downvote_from_reply(reply_id)
        reply_service.set_reaction_to_one(user_id, reply_id)
        reply_service.upvote_reply(reply_id)
        return JSONResponse(status_code=200, content=f'Upvote complete!')

    if not reply_service.check_reply_exists_by_id(reply_id):
        return JSONResponse(status_code=400, content=f'Wrong ID, no such reply!')
    else:
        reply_service.upvote_reply(reply_id)
        reply_service.add_upvote_to_reactions(user_id, reply_id)
        return JSONResponse(status_code=200, content=f'Upvote complete!')

    


@reply_router.put("/{reply_id}/downvote", description="Downvote a reply")
def downvote_reply(reply_id: int, x_token: str = Header()):
    user = get_user_or_raise_401(x_token)
    user_id, _ = x_token.split(_SEPARATOR)

    if reply_service.check_if_already_downvoted(user_id, reply_id):
        return JSONResponse(status_code=400, content=f'You already downvoted this reply!')
    
    if reply_service.check_if_already_upvoted(user_id, reply_id):
        reply_service.remove_upvote_from_reply(reply_id)
        reply_service.set_reaction_to_zero(user_id, reply_id)
        reply_service.downvote_reply(reply_id)
        return JSONResponse(status_code=200, content=f'Downvote complete!')

    if not reply_service.check_reply_exists_by_id(reply_id):
        return JSONResponse(status_code=400, content=f'Wrong ID, no such reply!')
    else:
        reply_service.downvote_reply(reply_id)
        reply_service.add_downvote_to_reactions(user_id, reply_id)
        return JSONResponse(status_code=200, content=f'Downvote complete!')
