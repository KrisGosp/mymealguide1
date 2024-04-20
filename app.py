from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import sqlite3
from helpers import login_required

# Initialize the Flask application
app = Flask(__name__)

# Connect to the database
conn = sqlite3.connect('database.db')
c = conn.cursor()

# c.execute(""" 
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         username TEXT NOT NULL,
#         hash TEXT NOT NULL
#     )""")
# c.execute("PRAGMA foreign_keys = ON")

# c.execute(""" 
#     CREATE TABLE IF NOT EXISTS recipes (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         user_id INTEGER,
#         name TEXT NOT NULL,
#         description TEXT,
#         total_time INTEGER,
#         category TEXT,
#         instructions TEXT,
#         difficulty INTEGER,
#         rating INTEGER,
#         FOREIGN KEY(user_id) REFERENCES users(id)
#     )""")
# c.execute("""
#     INSERT INTO recipes (name, description, total_time, category, instructions, difficulty, rating)
#     VALUES (?, ?, ?, ?, ?, ?, ?)
# """, ('amaa', 'lalal', 30, 'italian', 'cook amaa', 1, 5))

# c.execute("SELECT * FROM recipes")
# print(c.fetchall())

conn.commit()
conn.close()

@app.route('/')
@login_required
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'POST'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return 'POST'
    return render_template('register.html')