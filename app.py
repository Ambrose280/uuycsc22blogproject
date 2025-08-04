from flask import Flask
from databaseconnector import db
from flask_migrate import Migrate
from flask import jsonify
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Import models AFTER db is initialized
with app.app_context():
    from models import *

# Initialize Flask Migrate
migrate = Migrate(app, db)


@app.route('/')
def index():
    return jsonify({"message": "Hello, world!"})

if __name__ == '__main__':
    app.run(debug=True)