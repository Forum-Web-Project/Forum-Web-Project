from pydantic import BaseModel
from datetime import date


class User(BaseModel):
    id: int
    username: str
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