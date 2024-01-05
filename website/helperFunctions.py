import sqlite3


def get_all_menus(n):
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT id, title FROM menus  LIMIT 20 OFFSET (?-1)*20",(n))
            menus = [dict(row) for row in cur.fetchall()]
            return menus
    except Exception as e:
        print(f"Error in get_all_restaurant_types: {str(e)}")
        return []
        
def get_all_menus():
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT id, title FROM menus")
            menus = [dict(row) for row in cur.fetchall()]
            return menus
    except Exception as e:
        print(f"Error in get_all_restaurant_types: {str(e)}")
        return []

def get_menus_for_restaurant(restaurant_id):
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT id, title FROM menus WHERE restaurant_id=?",(restaurant_id,))
            menus = [dict(row) for row in cur.fetchall()]
            print(menus)
            return menus
    except Exception as e:
        print(f"Error in get_all_restaurant_types: {str(e)}")
        return []
    
def get_menus_for_page(page, per_page, sort_by, order):
    # Validate the sort_by parameter to prevent SQL injection
    allowed_sort_columns = ['id', 'title', 'price', 'restaurant_id', 'food_type_id']
    if sort_by not in allowed_sort_columns:
        raise ValueError("Invalid sort_by parameter")

    # Validate the order parameter to prevent SQL injection
    allowed_orders = ['asc', 'desc']
    if order not in allowed_orders:
        raise ValueError("Invalid order parameter")

    # Calculate the offset based on the page number and number of menus per page
    offset = (page - 1) * per_page

    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # Use the sort_by and order parameters in the ORDER BY clause
        cur.execute(f"SELECT menus.id as id, menus.title as title, menus.price as price, menus.description as description, restaurants.name as restaurant_name, restaurant_type.type as food_type FROM menus left join restaurants on restaurants.id = menus.restaurant_id left join restaurant_type on restaurant_type.id = menus.food_type_id ORDER BY {sort_by} {order} LIMIT ? OFFSET ?", (per_page, offset))
        menus = cur.fetchall()

    return menus

def get_total_menus():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(id) FROM menus")
        total_menus = cur.fetchone()[0]

    return total_menus


def get_orders_for_page(page, per_page, sort_by, order):
    # Validate the sort_by parameter to prevent SQL injection
    allowed_sort_columns = ['id', 'user_id', 'restaurant_id', 'menu_id', 'amount', 'created_at']
    if sort_by not in allowed_sort_columns:
        raise ValueError("Invalid sort_by parameter")

    # Validate the order parameter to prevent SQL injection
    allowed_orders = ['asc', 'desc']
    if order not in allowed_orders:
        raise ValueError("Invalid order parameter")

    # Calculate the offset based on the page number and number of orders per page
    offset = (page - 1) * per_page

    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # Use the sort_by and order parameters in the ORDER BY clause
        cur.execute(f"SELECT orders.id as id, orders.user_id as user_id, restaurants.name as restaurant_name, menus.title as menu_title, orders.amount as amount, orders.created_at as created_at FROM orders left join restaurants on restaurants.id = orders.restaurant_id left join menus on menus.id = orders.menu_id ORDER BY {sort_by} {order} LIMIT ? OFFSET ?", (per_page, offset))
        orders = cur.fetchall()

    return orders

def get_total_orders():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(id) FROM orders")
        total_orders = cur.fetchone()[0]

    return total_orders
    

def get_all_restaurants(sort_by='id', order='asc'):
    # Validate the sort_by parameter to prevent SQL injection
    allowed_sort_columns = ['id', 'name', 'restaurant_type_id', 'min_cost', 'rating', 'is_free_delivery', 'delivery_time', 'cost_level', 'status']
    if sort_by not in allowed_sort_columns:
        raise ValueError("Invalid sort_by parameter")

    # Validate the order parameter to prevent SQL injection
    allowed_orders = ['asc', 'desc']
    if order not in allowed_orders:
        raise ValueError("Invalid order parameter")

    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        print(order)
        # Use the sort_by and order parameters in the ORDER BY clause
        cur.execute(f"SELECT * FROM restaurants ORDER BY {sort_by} {order}")
        restaurants = cur.fetchall()

    return restaurants

def get_total_restaurants():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(id) FROM restaurants")
        total_restaurants = cur.fetchone()[0]

    return total_restaurants

def get_restaurant_by_id(restaurant_id):
    # Function to retrieve user details by ID from the database
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM restaurants WHERE id=?", (restaurant_id,))
        restaurant = cur.fetchone()
        return restaurant 

def get_restaurants_for_page(page, per_page, sort_by, order):
    # Validate the sort_by parameter to prevent SQL injection
    allowed_sort_columns = ['id', 'name', 'restaurant_type_id', 'min_cost', 'rating', 'is_free_delivery', 'delivery_time', 'cost_level', 'status']
    if sort_by not in allowed_sort_columns:
        raise ValueError("Invalid sort_by parameter")

    # Validate the order parameter to prevent SQL injection
    allowed_orders = ['asc', 'desc']
    if order not in allowed_orders:
        raise ValueError("Invalid order parameter")

    # Calculate the offset based on the page number and number of restaurants per page
    offset = (page - 1) * per_page

    with sqlite3.connect('database.db') as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        # Use the sort_by and order parameters in the ORDER BY clause
        cur.execute(f"SELECT restaurants.*, restaurant_type.type as restaurant_type FROM restaurants left join restaurant_type on restaurant_type.id = restaurants.restaurant_type_id  ORDER BY {sort_by} {order} LIMIT ? OFFSET ?", (per_page, offset))
        restaurants = cur.fetchall()

    return restaurants

def get_all_restaurant_types():
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute("SELECT id, type FROM restaurant_type")
            restaurant_types = [dict(row) for row in cur.fetchall()]
            return restaurant_types
    except Exception as e:
        print(f"Error in get_all_restaurant_types: {str(e)}")
        return []
    
  
def delete_related_restaurants(type_id):
    # Delete related restaurants from the database
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("DELETE FROM restaurants WHERE restaurant_type_id=?", (type_id,))
        con.commit()
        
def is_type_exist(type_name):
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("SELECT id FROM restaurant_type WHERE type=?", (type_name,))
            result = cur.fetchone()
            return result is not None
    except Exception as e:
        print(f"Error in is_type_exist: {str(e)}")
        return False

def is_user_exist(user_name):
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("SELECT user_name FROM users WHERE user_name=?", (user_name,))
            result = cur.fetchone()
            return result is not None
    except Exception as e:
        print(f"Error in is_type_exist: {str(e)}")
        return False

def get_user_by_id(user_id):
    # Function to retrieve user details by ID from the database
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
        user = cur.fetchone()
        return user  
    
def is_user_id_exist(user_id):
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("SELECT id FROM users WHERE id=?", (user_id,))
            result = cur.fetchone()
            return result is not None
    except Exception as e:
        print(f"Error in is_type_exist: {str(e)}")
        return False
    
def is_email_exist(email):
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("SELECT email FROM users WHERE email=?", (email,))
            result = cur.fetchone()
            return result is not None
    except Exception as e:
        print(f"Error in is_type_exist: {str(e)}")
        return False

    



    

    










    