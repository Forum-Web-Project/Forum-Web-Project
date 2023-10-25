from data.models import Topic, AllCategories, CategoryByID
from data.database import read_query, insert_query


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


def get_by_id(id: int):
    category_raw_data = read_query(
        'SELECT id, name, is_private FROM categories WHERE id = ?', (id,))

    if not category_raw_data:
        return None

    topics_raw_data = read_query(
        'SELECT id, title, text, users_id, categories_id FROM topics WHERE categories_id = ?', (id,))

    return CategoryByID.from_query_result(
        *category_raw_data[0],
        [Topic.from_query_result(*row) for row in topics_raw_data])

def read_categories():

    data = read_query('SELECT * FROM category')


    return data

def check_category_exists(id: int):
    data = read_query(
        'SELECT id FROM categories WHERE id = ?',
        (id,)
    )
