from data.database import read_query, update_query, insert_query

def read_categories():

    data = read_query('SELECT * FROM category')


    return data

def check_category_exists(id: int):
    data = read_query(
        'SELECT id FROM categories WHERE id = ?',
        (id,)
    )

    return bool(data)