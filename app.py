from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class User(Resource):

	def __init__(self, username, password, venmo, phone, rating, listings):
		self.username = username
		self.password = password
		self.venmo_id = venmo
		self.phone_number = phone
		self.rating = rating
		self.listings = listings #list of listings

	def post(self):

    def get(self):
        return {"hello": "world"}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)


import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from flask import jsonify

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def show_home():

@app.route('/user/create_account/<int: user_id', methods=[POST])
def create_account(username, password, venmo, ):

@app.route('/user/<int: user_id>', methods=[GET])
def user_info(user_id):
	users[user_id]



