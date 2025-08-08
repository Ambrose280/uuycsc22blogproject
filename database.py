import sqlite3
from flask import g, current_app

DATABASE = 'blog.db'

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            dbname=current_app.config['DB_NAME'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            host=current_app.config['DB_HOST'],
            port=current_app.config.get('DB_PORT', 5432),
            cursor_factory=RealDictCursor
        )
    return g.db

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
