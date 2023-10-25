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
    id: int
    title: str
    text: str
    username: str
    categories_id: int
    
    # @classmethod
    # def from_query_result(cls, id, title, text, users_id, categories_id):
    #     return cls(
    #         id=id,
    #         title=title,
    #         text=text,
    #         users_id=users_id,
    #         categories_id=categories_id)

class AllCategories(BaseModel):
    id: int
    name: str
    is_private: str

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
    def from_query_result(cls, id, name, is_private, topics):
        return cls(
            id=id,
            name=name,
            is_private=is_private,
            topics=topics or [])
    


class TopicForCategory(BaseModel):
    id: int
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