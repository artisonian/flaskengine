# all the imports
from flask import Flask
from flaskengine import settings
import mongoengine
import markdown

# helpers
def to_markdown(value):
    """Converts a string into valid Markdown."""
    return markdown.markdown(value)

def connect_db():
    """
    Connects to a running MongoDB instance and returns
    a database object.
    """
    return mongoengine.connect(settings.DATABASE)

# create our little application :)
app = Flask(__name__)
app.secret_key = settings.SECRET_KEY
app.debug = settings.DEBUG
app.jinja_env.filters['markdown'] = to_markdown

# import views
import flaskengine.views