from flask import Flask, redirect, render_template, request, session, g
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from helpers import login_required, apology

# Initialize the Flask application
app = Flask(__name__)

# Configure the Session for the Flask application
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to the database
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Implement thread-specific db connection
@app.before_request
def before_request():
    g.db = sqlite3.connect('database.db')
    g.c = g.db.cursor()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

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
        
    # Forget any user_id
    session.clear()

    if request.method == 'POST':
        if request.form.get('username') == '' or request.form.get('password') == '':
            return 'Please fill in all fields'
        
        uname = request.form.get('username')
        pword = generate_password_hash(request.form.get('password'))
        
        
    return render_template('login.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():

    # Forget any user_id
    session.clear()

    if request.method == 'POST':
        if not request.form.get('username') or not request.form.get('password'):
            return apology('Please fill in all fields', 400)

        uname = request.form.get('username')
        pword = generate_password_hash(request.form.get('password'))
        print(uname, pword)
        # Check if the username is already taken

        # Insert the user into the database
        g.c.execute('INSERT INTO users (username, hash) VALUES (?, ?)', (uname, pword))
        g.db.commit()
        return redirect('/login')
    return render_template('register.html')


# Close the database connection when the application is terminated
conn.commit()
conn.close()
