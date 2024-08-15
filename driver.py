## Main Project Flask Run Page

## Import "prefix" code into your Flask app to make your app usable when running
## Flask either in the csel.io virtual machine or running on your local machine.
## The module will create an app for you to use
import prefix
import sqlite3
from flask import Flask, request, url_for, make_response, render_template, jsonify, redirect

# create app to use in this Flask application
app = Flask(__name__)

# Insert the wrapper for handling PROXY when using csel.io virtual machine
# Calling this routine will have no effect if running on local machine
prefix.use_PrefixMiddleware(app)   

# test route to show prefix settings
@app.route('/prefix_url')  
def prefix_url():
    return 'The URL for this page is {}'.format(url_for('prefix_url'))

###############################################################################
## Required Routes for Project:
##
##     1. login page                  @app.route(/)
##     2. home page                   @app.route('/home')
##     3. leagues page                @app.route('/leagues')
##     4. mypicks page                @app.route('/mypicks')
##
################################################################################
@app.route('/')
def login():
    return "login page"

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