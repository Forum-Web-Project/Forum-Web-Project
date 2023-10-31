from pydantic import BaseModel, constr
from datetime import date

TUsername = constr(max_length=30, min_length=2)

class User(BaseModel):
    id: int
    username: TUsername
    password: str
    email: str
    role: str

    @classmethod
    def from_query_result(cls, id, username, password, email, role):
        return cls(
            id=id,
            username=username,
            password=password,
            email=email,
            role=role)
    

class LoginData(BaseModel):
    username: TUsername
    password: str
    email: str


class Topic(BaseModel):
    title: str
    text: str
    username: str
    category_id: int
    
    @classmethod
    def from_query_result(cls, id, title, text, users_id, categories_id):
        return cls(
            id=id,
            title=title,
            text=text,
            users_id=users_id,
            categories_id=categories_id)

class AllCategories(BaseModel):
    id: int
    name: str
    is_private: bool

    @classmethod
    def from_query_result(cls, id, name, is_private):
        return cls(
            id=id,
            name=name,
            is_private=is_private)
    
class CategoryByID(BaseModel):
    id: int
    name: str
    is_private: str
    topics: list = []

    
    @classmethod
    def from_query_result(cls, id, name, is_private, topics=None):
        return cls(
            id=id,
            name=name,
            is_private=is_private,
            topics=topics or [])

    
class Message(BaseModel):
    id: int
    text: str | None
    sender_id: int
    receiver_username: str

    @classmethod
    def from_query_result(cls, id, text, sender_id, receiver_username):
        return cls(
            id=id,
            text=text,
            sender_id=sender_id,
            receiver_username=receiver_username)
    
class Reply(BaseModel):
    text: str
    username: str
    topic_name: str
