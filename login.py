import app.py
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

@app.route('/login', methods=['GET', 'POST'])
def login():
    query = app.query_db('select username, password from users')
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
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))