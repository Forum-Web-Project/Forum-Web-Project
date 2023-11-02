from data.models import Topic, AllCategories, CategoryByID, User
from data.database import read_query, insert_query, update_query
from fastapi import APIRouter, Response, Header, HTTPException, Query, Depends
from services import user_service
from data.models import AllCategories
from sqlalchemy.orm import Session
import json
import re



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

def check_category_exists_for_topic(id: int):
    data = read_query(
        'SELECT id FROM categories WHERE id = ?',
        (id,)
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


def get_read_access_users(category_id: int):
    data = read_query(
        'SELECT read_access_users FROM categories WHERE id = ?',
        (category_id,)
    )

    if data[0][0] == None:
        return None
    
    pattern = r'[A-Za-z0-9]+'

    usernames = []
    for i in data[0]:
        name = re.findall(pattern, i)
        usernames.append(name)

    return usernames


def check_user_role(token: str, role: str = "Admin"):
    # Validate the token and retrieve the user
    user = user_service.from_token(token)

    # Check if the user has the required role
    if user.role != role:
        raise HTTPException(status_code=401, detail=f"Only {role}s can perform this action")


def get_categoryby_id(category_id: int) -> AllCategories | None:
    category_raw_data = read_query(
        'SELECT id, name, is_private FROM categories WHERE id = ?', (category_id,))

    if not category_raw_data:
        return None

    category = AllCategories.from_query_result(*category_raw_data[0])
    return category


def update_category_privacy(category_id: int, is_private: bool):
    category = get_categoryby_id(category_id)

    category.is_private = is_private
    update_query('UPDATE categories SET is_private = ? WHERE id = ?', (is_private, category_id))
    return category


def give_read_access_to_category(category_id: int, user_id: int):
    category = get_categoryby_id(category_id)    
    user = user_service.find_user_by_id(user_id)   

    if not category:
        raise ValueError(f"No category found with id {category_id}")
    if not user:
        raise ValueError(f"No user found with id {user_id}")


    category.read_access_users.append(user.username)

    read_access_users_json = json.dumps(category.read_access_users)

    update_query("UPDATE categories SET read_access_users = CASE WHEN read_access_users IS NULL OR JSON_UNQUOTE(read_access_users) = '[]' THEN JSON_ARRAY(?) ELSE JSON_ARRAY_APPEND(read_access_users, '$', ?) END WHERE id = ?;", (read_access_users_json, read_access_users_json, category_id))
    
    
def get_all_from_categoryby_id(category_id: int) -> AllCategories | None:
    category_raw_data = read_query(
        'SELECT * FROM categories WHERE id = ?', (category_id,))

    if not category_raw_data:
        return None

    category = AllCategories.from_query_result(*category_raw_data[0])
    return category


def is_category_private(id: str) -> bool:
    category = find_category_by_id(id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category.is_private
