# all the imports
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
import mongoengine
import markdown
import datetime

# configuration
DATABASE = 'flaskengine'
DEBUG = True    # DISABLE while in production
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# helpers
def to_markdown(value):
    """Converts a string into valid Markdown."""
    return markdown.markdown(value)

def connect_db():
    """
    Connects to a running MongoDB instance and returns
    a database object.
    """
    return mongoengine.connect(DATABASE)

# create our little application :)
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.debug = DEBUG
app.jinja_env.filters['markdown'] = to_markdown

# models
class Entry(mongoengine.Document):
    """An Entry document model."""
    title = mongoengine.StringField(required=True, max_length=200)
    text = mongoengine.StringField()
    created_at = mongoengine.DateTimeField(
        default=datetime.datetime.now())


# views
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
        if request.form['username'] != USERNAME:
            error = 'Invalid username'
        elif request.form['password'] != PASSWORD:
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


if __name__ == '__main__':
    app.run()
