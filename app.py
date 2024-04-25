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

CATEGORIES = ['Breakfast', 'Main', 'Dessert', 'Side', 'Snack']
COLUMNS = ['name', 'difficulty', 'rating', 'price', 'cooked']
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
    category = request.args.get('category')
    if category:
        rows = g.c.execute('SELECT id, name, category, difficulty, rating, price, last_cooked FROM recipes WHERE user_id = ? AND category = ?', (session['user_id'], category)).fetchall()
        return render_template('index.html', rows=rows, columns=COLUMNS, categories=CATEGORIES, category=category.capitalize())  
    else:
        rows = g.c.execute('SELECT id, name, category, difficulty, rating, price, last_cooked FROM recipes WHERE user_id = ?', (session['user_id'],)).fetchall()
        return render_template('index.html', rows=rows, columns=COLUMNS, categories=CATEGORIES)

# Authentication routes
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

# Sorting route
@app.route('/sort')
def sort():
    column = request.args.get('column', default='name').lower()
    way = request.args.get('way', default='ASC')
    category = request.args.get('category', default='').capitalize()
    if category:
        filtered = g.c.execute(f'SELECT id, name, category, difficulty, rating, price, last_cooked FROM recipes WHERE user_id = ? AND category = ?', (session['user_id'], category)).fetchall()
        return render_template('index.html', rows=filtered, columns=COLUMNS, categories=CATEGORIES, category=category) 
    if column == 'cooked':
        if way == 'ASC':
            rows = g.c.execute(f'SELECT id, name, category, difficulty, rating, price, last_cooked FROM recipes WHERE user_id = ? ORDER BY last_cooked', (session['user_id'],)).fetchall()
        elif way == 'DESC':
            rows = g.c.execute(f'SELECT id, name, category, difficulty, rating, price, last_cooked FROM recipes WHERE user_id = ? ORDER BY last_cooked DESC', (session['user_id'],)).fetchall()
        return render_template('index.html', rows=rows, columns=COLUMNS)
    if way == 'ASC':
        rows = g.c.execute(f'SELECT id, name, category, difficulty, rating, price, last_cooked FROM recipes WHERE user_id = ? ORDER BY {column}', (session['user_id'],)).fetchall()
    elif way == 'DESC':
        rows = g.c.execute(f'SELECT id, name, category, difficulty, rating, price, last_cooked FROM recipes WHERE user_id = ? ORDER BY {column} DESC', (session['user_id'],)).fetchall()

    return render_template('index.html', rows=rows, columns=COLUMNS, categories=CATEGORIES)

# Adding route
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
        if not name or not desc or not instructions or not difficulty or not category or not price or not rating:
            return apology('Please fill in all fields', 400)
        if not total_time or not total_time.isnumeric():
            total_time = 0
        if int(difficulty) not in [1, 2, 3]:
            return apology('Invalid difficulty', 400)
        if price not in ['$', '$$', '$$$']:
            return apology('Invalid price', 400)
        if int(rating) not in [1, 2, 3, 4, 5]:
            return apology('Invalid rating', 400)
        if category not in CATEGORIES:
            return apology('Invalid category', 400)
        last_cooked = date.today().isoformat()
        print(name, desc, instructions, difficulty, category, price, total_time, last_cooked, rating)
        g.c.execute('INSERT INTO recipes (user_id, name, description, total_time, category, instructions, difficulty, rating, price, last_cooked) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (session['user_id'], name, desc, total_time, category, instructions, difficulty, rating, price, last_cooked))
        g.db.commit()
        return redirect('/')
    return render_template('add.html', categories=CATEGORIES)

# Dynamic routes
@app.route('/recipe/<int:id>')
def recipe(id):
    row = g.c.execute('SELECT * FROM recipes WHERE id = ?', (id,)).fetchone()
    return render_template('recipe.html', row=row)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    recipe = g.c.execute('SELECT * FROM recipes WHERE id = ?', (id,)).fetchone()
    if recipe is None:
        return apology('Recipe not found', 404)
    
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

        g.c.execute('UPDATE recipes SET name = ?, description = ?, total_time = ?, category = ?, instructions = ?, difficulty = ?, rating = ?, price = ?, last_cooked = ? WHERE id = ?', (name, desc, total_time, category, instructions, difficulty, rating, price, last_cooked, id))
        g.db.commit()
        return redirect('/recipe/' + id)
    
    return render_template('update.html', recipe=recipe, categories=CATEGORIES)

@app.route('/delete/<int:id>')
def delete(id):
    g.c.execute('DELETE FROM recipes WHERE id = ?', (id,))
    g.db.commit()
    return redirect('/')

@app.route('/cooking_now/<int:id>')
def cooking_now(id):
    cooking = request.args.get('cooking')
    if cooking == 'yes':
        g.c.execute('UPDATE recipes SET last_cooked = ? WHERE id = ?', (date.today().isoformat(), id))
    
    g.db.commit()
    return redirect('/recipe/' + str(id))
# Close the database connection when the application is terminated
conn.commit()
conn.close()

