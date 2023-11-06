from fastapi import FastAPI
from routers.read_access_users import user_router
from routers.users import users_router
from routers.topics import topics_router
from routers.categories import category_router
from routers.messages import message_router
from routers.replies import reply_router


app = FastAPI()
app.include_router(users_router)
app.include_router(topics_router)
app.include_router(category_router)
app.include_router(message_router)
app.include_router(reply_router)
app.include_router(user_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host="127.0.0.1", port=8000, reload=True)