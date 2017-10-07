import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file , flaskr.py

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


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def show_home():
	db = get_db()
	return render_template('login.html', error=None)

@app.route('/user/<int:user_id>', methods=['POST'])
def create_account(name, username, password, venmo, phone_number):
    db = get_db()
    error = None
    usernames = db.execute('select username from users')
    if username in usernames:
    	error = 'username already exists. choose a new username.'
    cur = db.execute('insert into users (?, ?, ?, ?, ?)', [name, username, password, venmo, phone_number])
    entries = cur.fetchall()
    return render_template('create_account.html', error=error)

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
	db = get_db()
	cur = db.execute('select username, venmo, phone_number, rating, number_of_ratings from users where user_id = ?', [user_id])
	entries = cur.fetchall()
	return render_template('settings.html', error=error)

@app.route('/user/<int:user_id>', methods=['PATCH'])
def update_rating(user_id, new_rating):
	db = get_db()
	old_rating = db.execute('select rating from users where user_id = ?', [user_id])
	number_of_ratings = db.execute('select number_of_ratings from users where user_id = ?', [user_id])[0] + 1
	updated = (old_rating + new_rating)/number_of_ratings
	cur = db.execute('update users set rating = ?, number_of_ratings = ? where user_id = ?', [updated, number_of_ratings, user_id])
	entries = cur.fetchall()
	return 'success'

@app.route('/user/<int:user_id>', methods=['PATCH'])
def update_username(user_id, new_username):
	db = get_db()
	cur = db.execute('update users set username = ? where user_id = ?', [new_username, user_id])
	entries = cur.fetchall()
	return 'success'

@app.route('/user/<int:user_id>', methods=['PATCH'])
def update_venmo(user_id, new_venmo):
	db = get_db()
	cur = db.execute('update users set venmo = ? where user_id = ?', [new_venmo, user_id])
	entries = cur.fetchall()
	return 'success'


@app.route('/listings', methods=['GET'])
def get_listings():
    db = get_db()
    cur = db.execute('select user_id, meal_time, place, cost, status from listings order by listing_id desc')
    entries = cur.fetchall()
    return render_template('show_listings.html', error=None)


@app.route('/listings/<int:listing_id>', methods=['GET'])
def get_one_listing(listing_id):
    db = get_db()
    cur = db.execute('select user_id, meal_time, place, cost, status from listings where listing_id = ?', [listing_id])
    entries = cur.fetchall()
    return 'success'


@app.route('/listings', methods=['POST'])
def add_listing():
    db = get_db()
    db.execute('insert into listings (user_id, time, place, cost, status, user2_id) values (?, ?, ?, ?, ?, ?)',
               [request.form['user'], request.form['time'], request.form['place'], request.form['cost'], 'available', -1])
    db.commit()
    flash('New listing was successfully posted')
    return 'success'


@app.route('/listings', methods=['DELETE'])
def delete_listing(listing_id):
    db = get_db()
    db.execute('delete from listings where listing_id = ?', [listing_id])
    db.commit()
    return 'success'


@app.route('/listings/<int:listing_id>', methods=['PATCH'])
def update_listing_status(listing_id, new_status):
    db = get_db()
    cur = db.execute('update listings set status = ? where listing_id = ?', [new_status, listing_id])
    db.commit()
    flash('Listing was successfully modified')
    return 'success'


@app.route('/listings', methods=['GET'])
def get_listings_user(user_id):
    db = get_db()
    cur = db.execute(
        'select user_id, meal_time, place, cost, status from listings where user_id = ? order by listing_id desc',
        [user_id])
    entries = cur.fetchall()
    return 'success'


@app.route('/listings/<int:place>', methods=['GET'])
def get_listings_specific():
    db = get_db()
    cur = db.execute(
        'select user_id, meal_time, place, cost, status from listings where place = ? order by listing_id desc',
        [request.form['place']])
    entries = cur.fetchall()
    return 'success'


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        query = query_db('select username, password from users')
    except:
        error = "You don't have an account."
        return render_template('login.html', error=error)
    usernames = [(i['username'], i['password']) for i in query]
    error = None
    if request.method == 'POST':
        match = [i for i in usernames if i[0] == request.form['username']]
        if not match:
            error = 'Invalid username'
        elif request.form['password'] != match[0][1]:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_home'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_home'))
