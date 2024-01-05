from flask import Blueprint, render_template, request
from datetime import datetime
from website.helperFunctions import *
from website.helperFunctions import *
from website.helperFunctions import *
from website.helperFunctions import *

orders = Blueprint('orders', __name__)

@orders.route('/list_orders/', defaults={'page': 1}, methods=['GET'])
@orders.route('/list_orders/<int:page>', methods=['GET'])
def list_orders(page):
    try:
        per_page = 20  # Number of orders per page

        # Get the sort_by and order parameters from the query string
        sort_by = request.args.get('sort_by', 'id')
        order = request.args.get('order', 'asc')

        # Validate the sort_by parameter to prevent SQL injection
        allowed_sort_columns = ['id', 'user_id', 'restaurant_id', 'menu_id', 'amount', 'created_at']
        if sort_by not in allowed_sort_columns:
            raise ValueError("Invalid sort_by parameter")

        # Validate the order parameter to prevent SQL injection
        allowed_orders = ['asc', 'desc']
        if order not in allowed_orders:
            raise ValueError("Invalid order parameter")

        # Get the orders for the specified page with ordering
        orders = get_orders_for_page(page, per_page, sort_by, order)

        # Get the total number of orders for pagination
        total_orders = get_total_orders()

        # Calculate the total number of pages
        total_pages = ((total_orders) // per_page) + 1

        return render_template(
            "list_orders.html",
            orders=orders,
            page=page,
            total_pages=total_pages,
            sort_by=sort_by,
            order=order,
        )
    except Exception as e:
        return str(e)


@orders.route('/add_order', methods=['GET', 'POST'])
def add_order():
    try:
        if request.method == 'POST':
            # Get form data
            user_id = request.form['user_id']
            restaurant_id = int(request.form.get('restaurant_id'))
            menu_id = int(request.form.get('menu_id'))
            amount = int(request.form['amount'])
            if not is_user_id_exist(user_id):
                raise ValueError("User id does not exist.")
            elif amount == 0:
                raise ValueError("Amount should be greater than 0.")
            else:
                with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO orders (user_id, restaurant_id, menu_id, amount, created_at) VALUES (?, ?, ?, ?, ?)",
                                (user_id, restaurant_id, menu_id, amount, datetime.now()))

                    con.commit()
                    msg = "Record successfully added to the database"
                    return render_template('result.html', msg=msg, restaurants=get_all_restaurants())

        return render_template("add_order.html", restaurants=get_all_restaurants())
    except Exception as e:
        error_message = str(e)
        return render_template("add_order.html", error_message=error_message,restaurants=get_all_restaurants())
 
@orders.route("/edit_order", methods=['POST', 'GET'])
def edit_order():
    
    con = sqlite3.connect("database.db")
    try:
        id = request.form['order_id']
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT orders.restaurant_id as restaurant_id, orders.id as id, orders.user_id as user_id, restaurants.name as restaurant_name, menus.title as menu_title, orders.amount as order_amount FROM orders, restaurants, menus WHERE restaurants.id = orders.restaurant_id AND menus.id = orders.menu_id AND orders.id = ?", (id,))

        order = cur.fetchone()
        print(order)
        con.close()
        return render_template("edit_order.html", order=order,restaurants=get_all_restaurants(), menus=get_all_menus())
    except Exception as e:
        print(f"Error in the SELECT: {str(e)}")
        return render_template("edit_order.html", restaurants=get_all_restaurants(), menus=get_all_menus())


@orders.route('/edit_order_rec', methods=['POST','GET'])
def edit_order_rec():
    if request.method == 'POST':
        con = None  # Initialize con outside the try block
        try:
            id = request.form['id']
            name = request.form['name']
            restaurant_type_id = request.form['restaurant_type_id']
            min_cost = request.form['min_cost']
            rating = request.form['rating']
            is_free_delivery = request.form['is_free_delivery']
            delivery_time = request.form['delivery_time']
            cost_level = request.form['cost_level']
            status = request.form['status']

            con = sqlite3.connect('database.db')
            cur = con.cursor()
            cur.execute("UPDATE restaurants SET name=?, restaurant_type_id=?, min_cost=?, rating=?, is_free_delivery=?, delivery_time=?, cost_level=?, status=? WHERE id=?",
                        (name, restaurant_type_id, min_cost, rating, is_free_delivery, delivery_time, cost_level, status, id))

            con.commit()
            msg = "Record successfully edited in the database"
        except Exception as e:
            if con:
                con.rollback()
            msg = f"Error in the Edit: {str(e)}"
        finally:
            if con:
                con.close()
            return render_template('result.html', msg=msg)

@orders.route('/delete_order', methods=['POST'])
def delete_order():
    if request.method == 'POST':
        try:
            id = request.form['id']
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("DELETE FROM orders WHERE id=?", (id,))

                con.commit()
                msg = "Record successfully deleted from the database"
        except Exception as e:
            con.rollback()
            msg = f"Error in the DELETE: {str(e)}"
        finally:
            con.close()
            return render_template('result.html', msg=msg)