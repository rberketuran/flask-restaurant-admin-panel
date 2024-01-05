import sqlite3
from flask import Flask, render_template, request, redirect, Blueprint, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime 

from website.helperFunctions import *

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            email = request.form['email']
            first_name = request.form['firstName']
            last_name = request.form['lastName']
            user_name = request.form['userName']
            password1 = request.form['password1']
            password2 = request.form['password2']
            
            
            if is_email_exist(email):
                raise ValueError("Email already exists")
            elif is_user_exist(user_name):
                raise ValueError("Username already exists")
            elif len(email) < 4:
                raise ValueError("Email must be greater than 3 characters.")
            elif len(first_name) < 2:
                raise ValueError("First name must be greater than 1 character.")
            elif password1 != password2:
                raise ValueError("Passwords don\'t match.")
            elif len(password1) < 7:
                raise ValueError("Password must be at least 7 characters.")
            else:
                password1 = generate_password_hash(password1)
                with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute("INSERT INTO users (email, name, surname, user_name, password, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                                (email, first_name, last_name, user_name, password1, datetime.now()))
                    con.commit()

            msg = "User successfully signed up."
            return render_template('result.html', msg=msg)

        except Exception as e:
            error_message =  str(e)
            return render_template('signup.html', error_message=error_message)

    return render_template('signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            password = request.form.get('password')

            if is_email_exist(email):
                with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute("SELECT password FROM users WHERE email=?", (email,))
                    originalPass = cur.fetchone()
                if check_password_hash(originalPass, password):
                    flash('Logged in successfully!', category='success')
                    return redirect(url_for('/')) 
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email does not exist.', category='error')
            return redirect('/')  
        except Exception as e:
            error_message = f"Error during login: {str(e)}"
            return render_template('login.html', error_message=error_message)        

    return render_template("login.html", user=current_user)


