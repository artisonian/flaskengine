FlaskEngine v0.2.0
===

A replica of [Flaskr](http://flask.pocoo.org/docs/tutorial/ "Flaskr - Flask Tutorial"), using [MongoEngine](http://hmarr.com/mongoengine/ "MongoEngine Docs") for persistence.

## Getting Started

Clone the repository, install the requirements, then run the server.

    git clone git://github.com/artisonian/flaskengine.git
    pip install -r requirements.txt
    python flaskr.py

Then point your browser at http://127.0.0.1:5000/

## Requirements

* flask >= 0.2 (in development)
* mongoengine
* python-markdown

## TODO

* Combine `runserver.py` and `runtests.py` into a single `manage.py` script.
* Add support for editing and deleting entries.
* Add support for Markdown extensions.
* Add license.
* Improve authentication.