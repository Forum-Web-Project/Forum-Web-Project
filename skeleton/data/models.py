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
    users_id: int
    categories_id: int
    
    @classmethod
    def from_query_result(cls, id, title, text, users_id, categories_id):
        return cls(
            id=id,
            title=title,
            text=text,
            users_id=users_id,
            categories_id=categories_id)
    
class Category(BaseModel):
    name: str

    topics: list = []

    
    @classmethod
    def from_query_result(cls, id, name, topics=None):
        return cls(
            id=id,
            name=name,
            topics=topics or [])