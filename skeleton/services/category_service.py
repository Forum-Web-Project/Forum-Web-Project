from data.models import Topic, AllCategories, CategoryByID, User
from data.database import read_query, insert_query
from fastapi import APIRouter, Response, Header, HTTPException, Query, Depends
from services import user_service


def sort(categories: list[AllCategories], *, reverse=False):
    
    def sort_fn(c: AllCategories): return c.id

    return sorted(categories, key=sort_fn, reverse=reverse)


def all(search: str = None):
    if search is None:
        data = read_query(
            '''SELECT id, name, is_private
            FROM categories''')
    else:
        data = read_query(
            '''SELECT id, name, is_private
               FROM categories 
               WHERE name LIKE ?''', (f'%{search}%',))

    return (AllCategories.from_query_result(*row) for row in data)


# def get_by_id(id: int):
#     category_raw_data = read_query(
#         'SELECT id, name, is_private FROM categories WHERE id = ?', (id,))

#     if not category_raw_data:
#         return None

#     topics_raw_data = read_query(
#         'SELECT id, title, text, users_id, categories_id FROM topics WHERE categories_id = ?', (id,))

#     return CategoryByID.from_query_result(
#         *category_raw_data[0],
#         [TopicForCategory.from_query_result(*row) for row in topics_raw_data])

def read_categories():
    data = read_query('SELECT * FROM categories')

    return data


def check_category_exists(name: str):
    data = read_query(
        'SELECT name FROM categories WHERE name = ?',
        (name,)
    )

    return bool(data)


def get_category_id_by_name(name: str):
    data = read_query(
        'SELECT id FROM categories WHERE name = ?',
        (name,)
    )
    return data[0][0]


def get_category_name_by_id(id: int):
    data = read_query(
        'SELECT name FROM categories WHERE id = ?',
        (id,)
    )
    return data[0][0]


def find_category_by_id(id: int):
    data = read_query(
        "SELECT * FROM categories WHERE id = ?",
        (id,)
    )
    if data:
        return data[0]
    else:
        return None


def read_category():
    data = read_query('SELECT * FROM categories')
    return data


def get_categories_by_name(name_search: str):
    data = read_query(
        'SELECT * FROM categories WHERE name LIKE ?',
        (f"%{name_search}%",)
    )
    return data


def sort_categories(requirement: str):
    order_by = ''
    if requirement == "asc":
        order_by = 'name ASC'
    elif requirement == "desc":
        order_by = 'name DESC'
    data = read_query(f'SELECT * FROM categories ORDER BY {order_by}')
    return data


def create_category(name: str, is_private: bool) -> AllCategories | None:
    generated_id = insert_query(
        'INSERT INTO categories(name, is_private) VALUES (?,?)',
        (name, is_private))

    return AllCategories(id=generated_id, name=name, is_private=is_private)


def check_user_role(token: str, role: str = "Admin"):
    # Validate the token and retrieve the user
    user = user_service.from_token(token)

    # Check if the user has the required role
    if user.role != role:
        raise HTTPException(status_code=401, detail=f"Only {role}s can perform this action")
