from flask import Blueprint, render_template, request, redirect
from website.helperFunctions import *

restaurant_type = Blueprint('restaurant_type', __name__)

@restaurant_type.route("/enternewtype", methods=['GET', 'POST'])
def enternewtype():
    try:
        if request.method == 'POST':
            type_name = request.form['type_name']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()

                # Check if the restaurant type already exists
                cur.execute("SELECT id FROM restaurant_type WHERE type=?", (type_name,))
                existing_type = cur.fetchone()

                if existing_type:
                    raise ValueError("Restaurant type already exists")

                # Insert the restaurant type if it doesn't exist
                cur.execute("INSERT INTO restaurant_type (type) VALUES (?)", (type_name,))

                con.commit()
                msg = "Restaurant type successfully added to the database"
                return render_template('result.html', msg=msg)

        return render_template("restaurant_type.html")

    except Exception as e:
        error_msg = str(e) if str(e) else "Error adding restaurant type"
        return render_template("restaurant_type.html", error_msg=error_msg)


@restaurant_type.route("/listtypes")
def list_types():
    restaurant_types = get_all_restaurant_types()
    return render_template("list_types.html", restaurant_types=restaurant_types)

        
@restaurant_type.route("/edit_type", methods=['POST', 'GET'])
def edit_type():
    if request.method == 'POST':
        try:
            id = request.form['id']
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT * FROM restaurant_type WHERE id = ?", (id,))

            rows = cur.fetchall()
        except Exception as e:
            rows = None
            print(f"Error in the SELECT: {str(e)}")
        finally:
            con.close()
            return render_template("edit_type.html", restaurant_types=rows)



@restaurant_type.route("/edit_type_rec", methods=['POST'])
def edit_type_rec():
    try:
        id = request.form['id']
        new_type_name = request.form['type']

        # Check if the new type already exists
        if not is_type_exist(new_type_name):
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE restaurant_type SET type=? WHERE id=?", (new_type_name, id))
                con.commit()
                msg = "Restaurant Type successfully edited in the database"
                return render_template('result.html', msg=msg)
        else:
            msg = "Error: Restaurant Type already exists"
            return render_template('result.html', msg=msg)
    except Exception as e:
        msg = f"Error in the Edit: {str(e)}"
        return render_template('result.html', msg=msg)


@restaurant_type.route("/deletetype", methods=['POST'])
def deletetype():
    if request.method == 'POST':
        try:
            id = request.form['id']

            delete_related_restaurants(id)

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("DELETE FROM restaurant_type WHERE id=?", (id,))
                con.commit()
                msg = "Restaurant type successfully deleted from the database"
        except Exception as e:
            msg = f"Error in deleting restaurant type: {str(e)}"
        finally:
            return redirect("/listtypes")  