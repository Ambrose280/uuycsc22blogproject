from flask import Flask
from databaseconnector import db
from flask_migrate import Migrate
from flask import jsonify
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Import models AFTER db is initialized
with app.app_context():
    from models import *

# Initialize Flask Migrate
migrate = Migrate(app, db)

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/createpost', methods=['GET', 'POST'])
def createpost():
    return render_template('createpost.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

@app.route('/pageinfo', methods=['GET'])
def pageinfo():
    return render_template('pageinfo.html')

@app.route('/createpost', methods=['GET', 'POST'])
def createpost():
    return render_template('createpost.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)