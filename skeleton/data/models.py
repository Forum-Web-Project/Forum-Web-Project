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
    