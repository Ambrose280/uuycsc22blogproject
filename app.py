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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')




if __name__ == '__main__':
    app.run(debug=True)