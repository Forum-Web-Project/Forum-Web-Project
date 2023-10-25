from data.database import read_query, insert_query
from data.models import Category


def sort(categories: list[Category], *, reverse=False):
    
    def sort_fn(c: Category): return c.id

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

    return (Category.from_query_result(*row) for row in data)

