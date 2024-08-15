## Main Project Flask Run Page

## Import "prefix" code into your Flask app to make your app usable when running
## Flask either in the csel.io virtual machine or running on your local machine.
## The module will create an app for you to use
import sqlite3
from flask import Flask, request, url_for, make_response, render_template, jsonify, redirect, session, flash
from database import create_user, verify_user, create_user_table

# create app to use in this Flask application
app = Flask(__name__)

#make sure the user table exists
create_user_table()


###############################################################################
## Required Routes for Project:
##     
##     1. register page               @app.route(/register)
##     1. login page                  @app.route(/login)
##     2. home page                   @app.route('/home')
##     3. leagues page                @app.route('/leagues')
##     4. mypicks page                @app.route('/mypicks')
##
################################################################################

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        create_user(username, password)
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = verify_user(username, password)

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your credentials.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return "home page"

@app.route('/leagues')
def leagues():
    return "leagues page"

@app.route('/mypicks')
def mypicks():
    return "mypicks page"
    
###############################################################################
# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application 
    # on the local development server using port 3308 instead of port 5000.
    app.run(host='0.0.0.0', port=5757)