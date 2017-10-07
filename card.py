import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'card-me-in.db'),
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

# @app.route('/')
# def show_home():
# 	db = get_db()
# 	cur = 

@app.route('/user/create_account/<int: user_id>', methods=['POST'])
def create_account(name, username, password, venmo, phone_number):
    db = get_db()
    error = None
    usernames = db.execute('select username from users')[0]
    if username in usernames:
    	error = 'username already exists. choose a new username.'
    cur = db.execute('insert into users (?, ?, ?, ?, ?)', [name, username, password, venmo, phone_number])
    entries = cur.fetchall()
    return render_template('create_account.html', error=error)

@app.route('/user/<int: user_id>', methods=['GET'])
def get_user_info(user_id):
	db = get_db()
	cur = db.execute('select username, venmo, phone_number, rating, number_of_ratings from users where user_id = ?', [user_id])
	entries = cur.fetchall()
	return 'success'

@app.route('/user/<int: user_id>', methods=['PATCH'])
def update_rating(user_id, new_rating):
	db = get_db()
	old_rating = db.execute('select rating from users where user_id = ?', [user_id])[0]
	number_of_ratings = db.execute('select number_of_ratings from users where user_id = ?', [user_id])[0] + 1
	updated = (old_rating + new_rating)/number_of_ratings
	cur = db.execute('update users set rating = ?, number_of_ratings = ? where user_id = ?', [updated, number_of_ratings, user_id])
	entries = cur.fetchall()
	return 'success'

@app.route('/user/<int: user_id>', methods=['PATCH'])
def update_username(user_id, new_username):
	db = get_db()
	cur = db.execute('update users set username = ? where user_id = ?', [new_username, user_id])
	entries = cur.fetchall()
	return 'success'

@app.route('/user/<int: user_id>', methods=['PATCH'])
def update_venmo(user_id, new_venmo):
	db = get_db()
	cur = db.execute('update users set venmo = ? where user_id = ?', [new_venmo, user_id])
	entries = cur.fetchall()
	return 'success'


