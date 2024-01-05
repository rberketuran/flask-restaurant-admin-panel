from flask import Blueprint, render_template, request
from website.helperFunctions import *

restaurant = Blueprint('restaurant', __name__)


@restaurant.route('/list_restaurants/', defaults={'page': 1}, methods=['GET'])
@restaurant.route('/list_restaurants/<int:page>', methods=['GET'])
def list_restaurants(page):
    try:
        per_page = 20  # Number of restaurants per page

        # Get the sort_by and order parameters from the query string
        sort_by = request.args.get('sort_by', 'id')
        order = request.args.get('order', 'asc')

        # Validate the sort_by parameter to prevent SQL injection
        allowed_sort_columns = ['id', 'name', 'restaurant_type_id', 'min_cost', 'rating', 'is_free_delivery', 'delivery_time', 'cost_level', 'status']
        if sort_by not in allowed_sort_columns:
            raise ValueError("Invalid sort_by parameter")

        # Validate the order parameter to prevent SQL injection
        allowed_orders = ['asc', 'desc']
        if order not in allowed_orders:
            raise ValueError("Invalid order parameter")

        # Get the restaurants for the specified page with ordering
        restaurants = get_restaurants_for_page(page, per_page, sort_by, order)

        # Get the total number of restaurants for pagination
        total_restaurants = get_total_restaurants()

        # Calculate the total number of pages
        total_pages = ((total_restaurants) // per_page) + 1

        return render_template(
            "list_restaurants.html",
            restaurants=restaurants,
            page=page,
            total_pages=total_pages,
            sort_by=sort_by,
            order=order,
        )
    except Exception as e:
        return str(e)


@restaurant.route("/enternew", methods=['GET', 'POST'])
def enternew():
    try:
        # Fetch restaurant types when loading the form
        restaurant_types = get_all_restaurant_types()
        if request.method == 'POST':
            # If it's a POST request, it means the form is submitted
            name = request.form['name']
            restaurant_type_id = request.form.get('restaurant_type_id')
            min_cost = request.form['min_cost']
            rating = request.form['rating']
            is_free_delivery = request.form.get('is_free_delivery', 0)
            delivery_time = request.form['delivery_time']
            cost_level = request.form['cost_level']
            status = request.form['status']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO restaurants (name, restaurant_type_id, min_cost, rating, is_free_delivery, delivery_time, cost_level, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (name, restaurant_type_id, min_cost, rating, is_free_delivery, delivery_time, cost_level, status))

                con.commit()
                msg = "Record successfully added to the database"
                restaurant_types = get_all_restaurant_types()

                return render_template('result.html', msg=msg, restaurant_types=restaurant_types)

        return render_template("restaurant.html", restaurant_types=restaurant_types)

    except Exception as e:
        print(f"Error in enternew: {str(e)}")
        return render_template("restaurant.html", restaurant_types=[])
    

@restaurant.route("/edit", methods=['POST', 'GET'])
def edit():
    if request.method == 'POST':
        try:
            id = request.form['id']
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT * FROM restaurants WHERE id = ?", (id,))

            rows = cur.fetchall()
        except Exception as e:
            rows = None
            print(f"Error in the SELECT: {str(e)}")
        finally:
            con.close()
            return render_template("edit_restaurants.html", restaurants=rows, restaurant_types=get_all_restaurant_types())
        

# Route used to execute the UPDATE statement on a specific record in the database
@restaurant.route("/editrec", methods=['POST', 'GET'])
def editrec():
    if request.method == 'POST':
        con = None 
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
        
# Route used to DELETE a specific record in the database    
@restaurant.route("/delete", methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        try:
            id = request.form['id']
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("DELETE FROM restaurants WHERE id=?", (id,))

                con.commit()
                msg = "Record successfully deleted from the database"
        except Exception as e:
            con.rollback()
            msg = f"Error in the DELETE: {str(e)}"
        finally:
            con.close()
            return render_template('result.html', msg=msg)