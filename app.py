from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from helpers import login_required

# Initialize the Flask application
app = Flask(__name__)

# Configure the Session for the Flask application
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to the database
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# Index route
@app.route('/')
@login_required
def home():
    return render_template('index.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'POST'
    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form.get('username') == '' or request.form.get('password') == '':
            return 'Please fill in all fields'
        
        uname = request.form.get('username')
        pword = generate_password_hash(request.form.get('password'))

        # Check if the username is already taken

        # Insert the user into the database
        c.execute('INSERT INTO users (username, hash) VALUES (?, ?)', (uname, pword))
        return redirect('/login')
    return render_template('register.html')


# Close the database connection when the application is terminated
conn.commit()
conn.close()