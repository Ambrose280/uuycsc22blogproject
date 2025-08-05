from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database import get_db, close_connection, init_db
from functools import wraps
from flask import g
import os
import re

import sqlite3
import secrets
import hashlib

from datetime import datetime
app = Flask(__name__)

app.secret_key = 'uuycscs@#1234'

@app.before_request
def set_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)

app.jinja_env.globals['csrf_token'] = lambda: session.get('csrf_token')


@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=session.get('csrf_token'))

@app.context_processor
def inject_user():
    db = get_db()
    user = None
    if 'user_id' in session:
        user = db.execute(
            'SELECT * FROM user WHERE id = ?',
            (session['user_id'],)
        ).fetchone()
    return dict(user=user)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()

def get_post_by_id(post_id):
    conn = sqlite3.connect('blog.db')  # replace with your actual DB path
    conn.row_factory = sqlite3.Row  # So you can access columns by name
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            post.*, 
            category.name as category_name,
            user.username as author_name
        FROM post 
        LEFT JOIN category ON post.category_id = category.id
        LEFT JOIN user ON post.user_id = user.id
        WHERE post.id = ?
    """, (post_id,))
    post = cur.fetchone()
    conn.close()
    return post

UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('upload')
    if not f:
        return jsonify(uploaded=0, error={'message': 'No file uploaded'})

    filepath = os.path.join(UPLOAD_FOLDER, f.filename)
    f.save(filepath)

    file_url = url_for('static', filename=f'uploads/{f.filename}')
    return jsonify(uploaded=1, fileName=f.filename, url=file_url)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def simple_secure_filename(filename):
    # Remove anything not alphanumeric, dash, underscore or dot
    filename = re.sub(r'[^A-Za-z0-9_.-]', '', filename)
    return filename


@app.route('/editpost/<int:post_id>', methods=['GET', 'POST'])
@login_required
def editpost(post_id):
    db = get_db()

    post = db.execute("SELECT * FROM post WHERE id = ?", (post_id,)).fetchone()
    if not post:
        return "Post not found", 404

    if post['user_id'] != session['user_id']:
        return "Unauthorized", 403

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        draft = bool(request.form.get('draft'))
        category_id = request.form.get('category_id')

        featured_image = post['featured_image']
        if 'featured_image' in request.files:
            image = request.files['featured_image']
            if image and image.filename:
                image_path = os.path.join('static/images', image.filename)
                image.save(image_path)
                featured_image = image.filename

        db.execute("""
            UPDATE post
            SET title = ?, body = ?, draft = ?, category_id = ?, featured_image = ?
            WHERE id = ?
        """, (title, content, draft, category_id, featured_image, post_id))
        db.commit()

        return redirect(url_for('index'))

    categories = db.execute("SELECT * FROM category").fetchall()
    return render_template('editpost.html', post=post, categories=categories)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # CSRF Validation
        token = request.form.get('csrf_token')
        if not token or token != session.get('csrf_token'):
            return "CSRF validation failed", 400

        # Form Data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']



        # Insert into DB
        db = get_db()
        try:
            db.execute(
                'INSERT INTO user (username, email, password) VALUES (?, ?, ?)',
                (username, email, password)
            )
            db.commit()
        except sqlite3.IntegrityError:
            return "Username or email already exists", 400

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/add-category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        # CSRF validation
        token = request.form.get('csrf_token')
        if not token or token != session.get('csrf_token'):
            return "CSRF validation failed", 400

        name = request.form['name'].strip()

        db = get_db()
        try:
            db.execute('INSERT INTO category (name) VALUES (?)', (name,))
            db.commit()
        except sqlite3.IntegrityError:
            return render_template("add_category.html", error="Category already exists", csrf_token=session['csrf_token'])

        return redirect(url_for('createpost'))

    return render_template("add_category.html", csrf_token=session['csrf_token'])




@app.route('/post/<int:post_id>', methods=['GET'])
def view_post(post_id):
    db = get_db()
    
    post = db.execute("""
        SELECT post.*, user.username, category.name as category_name
        FROM post
        JOIN user ON post.user_id = user.id
        LEFT JOIN category ON post.category_id = category.id
        WHERE post.id = ?
    """, (post_id,)).fetchone()
    
    if not post:
        return "Post not found", 404

    comments = db.execute("""
        SELECT comment.*, user.username 
        FROM comment
        JOIN user ON comment.user_id = user.id
        WHERE comment.post_id = ?
        ORDER BY comment.timestamp DESC
    """, (post_id,)).fetchall()

    user = session.get('user')  # Assuming user is stored in session

    return render_template('postdetail.html', post=post, comments=comments, user=user)



@app.route('/post/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    user = g.user
    if not user:
        return redirect(url_for('login'))

    text = request.form.get('text')
    if not text:
        return "Comment text is required", 400

    db = get_db()
    db.execute("""
        INSERT INTO comment (post_id, user_id, text, timestamp)
        VALUES (?, ?, ?, ?)
    """, (post_id, user['id'], text, datetime.utcnow()))
    db.commit()

    return redirect(url_for('view_post', post_id=post_id))



@app.route('/createpost', methods=['GET', 'POST'])
@login_required
def createpost():
    db = get_db()

    if request.method == 'POST':
        token = request.form.get('csrf_token')
        if not token or token != session.get('csrf_token'):
            return "CSRF validation failed", 400

        user_id = session['user_id']
        title = request.form['title']
        content = request.form['content']
        draft = bool(request.form.get('draft'))
        category_id = request.form.get('category_id') or None  # Allow null

        # Handle featured image
        featured_image = None
        if 'featured_image' in request.files:
            image = request.files['featured_image']
            if image and image.filename:
                image_path = os.path.join('static/images', image.filename)
                image.save(image_path)
                featured_image = image.filename

        db.execute("""
            INSERT INTO post (title, body, draft, user_id, category_id, featured_image)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, content, draft, user_id, category_id, featured_image))
        db.commit()

        return redirect(url_for('index'))

    # Fetch categories for dropdown
    categories = db.execute("SELECT id, name FROM category").fetchall()
    return render_template('createpost.html', categories=categories, csrf_token=session['csrf_token'])



@app.route('/')
def index():
    db = get_db()
    search = request.args.get('search', '').strip()
    category_id = request.args.get('category_id')

    query = """
        SELECT 
            post.id, post.title, post.timestamp, post.featured_image,
            user.username,
            category.name AS category_name,
            (SELECT COUNT(*) FROM comment WHERE comment.post_id = post.id) AS comment_count
        FROM post
        JOIN user ON post.user_id = user.id
        LEFT JOIN category ON post.category_id = category.id
        WHERE post.draft = 0
    """

    params = []

    if search:
        query += " AND post.title LIKE ?"
        params.append(f'%{search}%')

    if category_id:
        query += " AND post.category_id = ?"
        params.append(category_id)

    query += " ORDER BY post.timestamp DESC"

    posts = db.execute(query, params).fetchall()
    categories = db.execute("SELECT id, name FROM category").fetchall()

    return render_template('index.html', posts=posts, categories=categories, search=search, category_id=category_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    db = get_db()

    if request.method == 'POST':
        token = request.form.get('csrf_token')
        if not token or token != session.get('csrf_token'):
            return "CSRF validation failed", 400

        username = request.form.get('username')
        password = request.form.get('password')

        user = db.execute(
            'SELECT * FROM user WHERE username = ? AND password = ?',
            (username, password)
        ).fetchone()

        if user:
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        return render_template('login.html', error='Invalid credentials', csrf_token=session['csrf_token'])

    session['csrf_token'] = secrets.token_hex(16)
    return render_template('login.html', csrf_token=session['csrf_token'])


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# if __name__ == '__main__':
#     if not os.path.exists('blog.db'):
#         with app.app_context():
#             init_db()
#     app.run(debug=True, host='0.0.0.0', port=5000)
