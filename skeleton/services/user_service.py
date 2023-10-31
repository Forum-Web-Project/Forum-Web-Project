from data.database import read_query,insert_query
from data.models import User

_SEPARATOR = ';'

def try_login(username: str, password: str) -> User | None:
    user = find_by_username(username)

    return user if user and user.password == password else None

def create_token(user: User) -> str:
    return f'{user.id}{_SEPARATOR}{user.username}'


def is_authenticated(token: str) -> bool:
    return any(read_query(
        'SELECT 1 FROM users WHERE id = ? and username = ?',
        token.split(_SEPARATOR)))


def from_token(token: str) -> User | None:
    _, nickname = token.split(_SEPARATOR)

    return find_by_username(nickname)

def find_by_username(nickname: str) -> User | None:
    data = read_query(
        'SELECT * FROM users WHERE username = ?',
        (nickname,))

    return next((User.from_query_result(*row) for row in data), None)

def create_user(username: str, password: str, email: str) -> User | None:
    # password = _hash_password(password)
        ROLE = "User"
        generated_id = insert_query(
            'INSERT INTO users(username, password, email, role) VALUES (?,?,?,?)',
            (username, password, email, ROLE))

        return User(id=generated_id, username=username, password="", email=email, role=ROLE)

def check_username_exist(nickname:str) -> bool:

    data = read_query(
        'SELECT username FROM users WHERE username = ?',
        (nickname,)
    )

    return bool(data)
    
def get_nickname_from_token(token: str) -> User | None:
    _, nickname = token.split(_SEPARATOR)

    return nickname

def find_username_by_id(id: int):
     data = read_query(
          "SELECT username FROM users WHERE id = ?",
          (id,)
    )
     return data[0][0]