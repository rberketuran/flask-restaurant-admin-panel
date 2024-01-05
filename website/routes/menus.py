from flask import Blueprint, render_template, request
import sqlite3
from datetime import datetime 
from website.helperFunctions import *
from website.helperFunctions import get_all_restaurant_types, get_all_restaurants

menus = Blueprint('menus', __name__)

@menus.route('/get_menus')
def get_menus():
    restaurant_id = request.args.get('restaurant_id')
    menus = get_menus_for_restaurant(restaurant_id)
    
    # Generate HTML options for the menus
    menu_options = ''.join([f'<option value="{menu["id"]}">{menu["title"]}</option>' for menu in menus])
    
    return menu_options

@menus.route("/add_menu", methods=['GET', 'POST'])
def add_menu():
    try:
        # Fetch restaurant types when loading the form
        restaurants = get_all_restaurants()
        if request.method == 'POST':
            # If it's a POST request, it means the form is submitted
            title = request.form['title']
            price = request.form.get('price')
            description = request.form['description']
            restaurant_id = request.form.get('restaurant_id')
            print(restaurants)
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("SELECT restaurant_type_id FROM restaurants WHERE id=?",(restaurant_id,))
                food_type_id = cur.fetchone()[0]
                print(food_type_id)
                cur.execute("INSERT INTO menus ( title , price , description , restaurant_id , food_type_id , created_at)  VALUES (?, ?, ?, ?, ?, ?)",
                            (title, price, description, restaurant_id, food_type_id, datetime.now()))

                con.commit()
                msg = "Record successfully added to the database"

                return render_template('result.html', msg=msg, restaurants=restaurants)

        return render_template("add_menu.html", restaurants=restaurants)

    except Exception as e:
        print(f"Error in add menu: {str(e)}")
        return render_template("add_menu.html", restaurants=restaurants)

@menus.route('/list_menus/', defaults={'page': 1}, methods=['GET'])
@menus.route('/list_menus/<int:page>', methods=['GET'])
def list_menus(page):
    try:
        per_page = 20  # Number of menus per page

        # Get the sort_by and order parameters from the query string
        sort_by = request.args.get('sort_by', 'id')
        order = request.args.get('order', 'asc')

        # Validate the sort_by parameter to prevent SQL injection
        allowed_sort_columns = ['id', 'title', 'price', 'restaurant_id', 'food_type_id']
        if sort_by not in allowed_sort_columns:
            raise ValueError("Invalid sort_by parameter")

        # Validate the order parameter to prevent SQL injection
        allowed_orders = ['asc', 'desc']
        if order not in allowed_orders:
            raise ValueError("Invalid order parameter")

        # Get the menus for the specified page with ordering
        menus = get_menus_for_page(page, per_page, sort_by, order)

        # Get the total number of menus for pagination
        total_menus = get_total_menus()

        # Calculate the total number of pages
        total_pages = ((total_menus) // per_page) + 1

        return render_template(
            "list_menus.html",
            menus=menus,
            page=page,
            total_pages=total_pages,
            sort_by=sort_by,
            order=order
        )
    except Exception as e:
        return str(e)  

@menus.route("/edit_menu", methods=['POST', 'GET'])
def edit_menu():
    if request.method == 'POST':
        try:
            id = request.form['id']
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT * FROM menus WHERE id = ?", (id,))

            rows = cur.fetchall()
        except Exception as e:
            rows = None
            print(f"Error in the SELECT: {str(e)}")
        finally:
            con.close()
            return render_template("edit_menu.html", menus=rows, restaurant_types=get_all_restaurant_types(), restaurants=get_all_restaurants())
        
@menus.route("/edit_menu_rec", methods=['POST', 'GET'])
def edit_menu_rec():
     if request.method == 'POST':
        con = None  
        try:
            id = request.form['id']
            title = request.form['title']
            restaurant_id = request.form['restaurant_id']
            price = request.form['price']
            description = request.form['description']
            food_type_id = request.form.get('food_type_id')

            con = sqlite3.connect('database.db')
            cur = con.cursor()
            cur.execute("UPDATE menus SET title=?, restaurant_id=?, price=?, description=?, food_type_id=? WHERE id=?",
                        (title, restaurant_id, price, description, food_type_id, id))

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

@menus.route("/delete_menu", methods=['POST', 'GET'])
def delete_menu():
    if request.method == 'POST':
        try:
            id = request.form['id']
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("DELETE FROM menus WHERE id=?", (id,))

                con.commit()
                msg = "Record successfully deleted from the database"
        except Exception as e:
            con.rollback()
            msg = f"Error in the DELETE: {str(e)}"
        finally:
            con.close()
            return render_template('result.html', msg=msg)


