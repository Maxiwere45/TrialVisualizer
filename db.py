import hashlib

import pymongo
import click
from flask import current_app, g

MONGO_URI = 'mongodb+srv://nrm4206a:9dfe351b@dbsae.ohuhcxc.mongodb.net/?retryWrites=true&w=majority'
def get_db():
    if 'db' not in g:
        client = pymongo.MongoClient(MONGO_URI)
        g.db = client['trial_visualizer']
    return g.db


def get_trial():
    db = get_db()
    return list(db['ClinicalTrials'].find().limit(1300).sort('id', pymongo.DESCENDING))
def get_trial_obstudies():
    db = get_db()
    return list(db['ClinicalTrials'].find({'trial_type': 'cl_obstudies'}))

def get_trial_randtrials():
    db = get_db()
    return list(db['ClinicalTrials'].find({'trial_type': 'cl_randtrials'}))

def get_publication():
    db = get_db()
    return list(db['Publications'].find())

def get_publication_obstudies():
    db = get_db()
    return list(db['Publications'].find({'p_type': 'p_obstudies'}))

def get_publication_randtrials():
    db = get_db()
    return list(db['Publications'].find({'p_type': 'p_randtrials'}))

def init_db():
    mdp = hashlib.sha256("9dfe351b".encode()).hexdigest()
    dbname = "trial_visualizer"
    client = pymongo.MongoClient(MONGO_URI)
    db = client[dbname]
    myCol = db["users"]
    x = myCol.insert_one({"username": "nrm4206a","password": mdp})
    if "users" in db.list_collection_names():
        print("Collection crée !")
    else:
        print("Collection non crée !")

    if x.inserted_id:
        print("Insertion réussie !")
    else:
        print("Insertion non réussie !")
    client.close()

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.client.close()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')