from flask import Flask, redirect, render_template, request, session, g
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
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

# Hopefully last alter of the table
# c.execute("""
# CREATE TABLE recipes (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         user_id INTEGER,
#         name TEXT NOT NULL,
#         description TEXT,
#         total_time INTEGER,
#         category TEXT,
#         instructions TEXT,
#         difficulty INTEGER,
#         rating INTEGER,
#         price TEXT,
#         last_cooked DATE,
#         FOREIGN KEY(user_id) REFERENCES users(id)
#     );""")

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
    rows = g.c.execute('SELECT name, category, difficulty, rating, price  FROM recipes WHERE user_id = ?', (session['user_id'],)).fetchall()
    return render_template('index.html', rows=rows)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
        
    # Forget any user_id
    session.clear()

    if request.method == 'POST':
        if request.form.get('username') == '' or request.form.get('password') == '':
            return apology('Please fill in all fields', 400)
        
        uname = request.form.get('username')
        rows = g.c.execute('SELECT * FROM users WHERE username = ?', (uname,)).fetchone()
        
        if not rows:
            return apology('Invalid username and/or password', 400)
        elif not check_password_hash(rows[2], request.form.get('password')):
            return apology('Invalid username and/or password', 400)

        # Remember user that has logged in
        session['user_id'] = rows[0]
        session['username'] = rows[1]

        return redirect('/')
        
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

        # Check if the username is already taken
        g.c.execute('SELECT * FROM users WHERE username = ?', (uname,))
        if g.c.fetchone() is not None:
            return apology('Username already taken', 400)

        # Insert the user into the database
        g.c.execute('INSERT INTO users (username, hash) VALUES (?, ?)', (uname, pword))
        g.db.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form.get('name')
        desc = request.form.get('desc')
        instructions = request.form.get('instructions')
        difficulty = request.form.get('difficulty')
        category = request.form.get('category')
        price = request.form.get('price')
        total_time = request.form.get('total_time')
        rating = request.form.get('option')
        last_cooked = date.today().isoformat()
        print(name, desc, instructions, difficulty, category, price, total_time, last_cooked, rating)
        g.c.execute('INSERT INTO recipes (user_id, name, description, total_time, category, instructions, difficulty, rating, price, last_cooked) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (session['user_id'], name, desc, total_time, category, instructions, difficulty, rating, price, last_cooked))
        g.db.commit()
        return redirect('/')
    return render_template('add.html')


# Close the database connection when the application is terminated
conn.commit()
conn.close()

