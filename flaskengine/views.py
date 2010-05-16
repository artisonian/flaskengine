from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
from flaskengine import app, connect_db, settings
from flaskengine.models import Entry

@app.before_request
def before_request():
    g.db = connect_db()

# @app.after_request
# def after_request(response):
#     g.db.connection.disconnect()
#     return response

@app.route('/')
def show_entries():
    entries = Entry.objects.order_by('-created_at')
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    entry = Entry(title=request.form['title'],
        text=request.form['text'])
    entry.save()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != settings.USERNAME:
            error = 'Invalid username'
        elif request.form['password'] != settings.PASSWORD:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You have been logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out')
    return redirect(url_for('show_entries'))