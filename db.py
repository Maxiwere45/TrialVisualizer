import pymongo
import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        client = pymongo.MongoClient(current_app.config['MONGO_URI'])
        g.db = pymongo.MongoClient(current_app.config['MONGO_DBNAME'])
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.client.close()

def init_app(app):
    app.teardown_appcontext(close_db)
