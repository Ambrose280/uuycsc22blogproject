import sqlite3
from flask import g, current_app

DATABASE = 'blog.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row 
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with current_app.app_context():
        db = get_db()
        with open('schema.sql', 'r') as f:
            db.executescript(f.read())
        print("Initialized the database.")
