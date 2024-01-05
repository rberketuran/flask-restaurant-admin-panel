from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime 
from website.helperFunctions import *

users = Blueprint('users', __name__)

@users.route("/add_user", methods=['GET', 'POST'])
def add_user():
    try:
        if request.method == 'POST':
            # If it's a POST request, it means the form is submitted
            email = request.form['email']
            user_name = request.form.get('user_name')
            password = request.form['password']
            name = request.form['name']
            surname = request.form.get('surname')
            password = generate_password_hash(password)
            if is_email_exist(email):
                raise ValueError("Email already exists")
            elif is_user_exist(user_name):
                raise ValueError("Username already exists")
            elif len(email) < 4:
                raise ValueError("Email must be greater than 3 characters.")
            elif len(name) < 2:
                raise ValueError("First name must be greater than 1 character.")
            else:
                with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO users ( email , password , user_name , name , surname , created_at ) VALUES ( ?, ?, ?, ?, ?, ?)",
                                (email, password, user_name, name, surname, datetime.now()))

                    con.commit()
                    msg = "Record successfully added to the database"

                    return render_template('result.html', msg=msg)

        return render_template("add_user.html")

    except Exception as e:
        error_message = str(e)
        return render_template("add_user.html", error_message=error_message)
    
@users.route('/list_users')
def list_users():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM users")

    rows = cur.fetchall()
    con.close()
    return render_template("list_users.html", users=rows)

@users.route("/edit_user", methods=['POST', 'GET'])
def edit_user():
    if request.method == 'POST':
        try:
            id = request.form['id']
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id = ?", (id,))

            rows = cur.fetchall()
        except Exception as e:
            rows = None
            print(f"Error in the SELECT: {str(e)}")
        finally:
            con.close()
            return render_template("edit_user.html", users=rows)

@users.route("/edit_user_rec", methods=['POST', 'GET'])
def edit_user_rec():
    if request.method == 'POST':
        con = None  # Initialize con outside the try block
        try:
            id = request.form['id']
            email = request.form['email']
            user_name = request.form.get('user_name')
            password = request.form['password']
            name = request.form['name']
            surname = request.form.get('surname')
            password = generate_password_hash(password)

            con = sqlite3.connect('database.db')
            cur = con.cursor()
            cur.execute("UPDATE users SET email=?, password=?, user_name=?, name=?, surname=?, created_at=? WHERE id=?",
                        (email, password, user_name, name, surname, datetime.now(), id))

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

@users.route('/delete_user', methods=['POST'])
def delete_user():
    try:
        user_id = request.form['id']

        # Perform the delete operation in the database
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("DELETE FROM users WHERE id=?", (user_id,))
            con.commit()

        return redirect(url_for('list_users'))

    except Exception as e:
        print(f"Error in delete_user: {str(e)}")
        return redirect(url_for('list_users'))

