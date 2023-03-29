import pymongo
from flask import g

MONGO_URI = 'mongodb+srv://nrm4206a:9dfe351b@dbsae.ohuhcxc.mongodb.net/?retryWrites=true&w=majority'


def get_db():
    if 'db' not in g:
        client = pymongo.MongoClient(MONGO_URI)
        g.db = client['trial_visualizer']
    return g.db


def get_trial():
    db = get_db()
    return list(db['ClinicalTrials'].find().limit(1300))


def get_trial_obstudies():
    db = get_db()
    return list(db['ClinicalTrials'].find({'trial_type': 'cl_obstudies'}).limit(1300))


def get_trial_randtrials():
    db = get_db()
    return list(db['ClinicalTrials'].find({'trial_type': 'cl_randtrials'}).limit(1300))


def get_publication():
    db = get_db()
    return list(db['Publications'].find().limit(1300))


def get_publication_obstudies():
    db = get_db()
    return list(db['Publications'].find({'p_type': 'p_obstudies'}).limit(1300))


def get_publication_randtrials():
    db = get_db()
    return list(db['Publications'].find({'p_type': 'p_randtrials'}).limit(1300))


# Nombre d'essais en phase 1 / 2 / 3 / 4
def get_phase_by_nb():
    db = get_db()
    return list(db['ClinicalTrials'].aggregate([
        {
            "$group": {
                "_id": "$phase",
                "count": {
                    "$sum": 1
                }
            }
        },
        {"$sort": {"count": -1}}
    ]))


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.client.close()


def init_app(app):
    app.teardown_appcontext(close_db)


def get_total_essais():
    db = get_db()
    return len(list(db['ClinicalTrials'].find()))


def get_total_esais_fem():
    db = get_db()
    return len(list(db['ClinicalTrials'].find({'gender': 'Female'})))


def get_total_esais_male():
    db = get_db()
    return len(list(db['ClinicalTrials'].find({'gender': 'Male'})))

def get_total_pub():
    db = get_db()
    return len(list(db['Publications'].find({})))

def get_total_pub_essais_rand():
    db = get_db()
    return db['Publications'].count_documents({'p_type': 'p_randtrials'})

def get_total_pub_essais_obs():
    db = get_db()
    return db['Publications'].count_documents({'p_type': 'p_obstudies'})

def get_top_concepts_by_publication_count(year):
    db = get_db()
    pipeline = [
        { "$unwind": "$concepts" },
        { "$group": {"_id": "$concepts", "count": {"$sum": 1}}},
        { "$match": {"openAccess": {"$not": {"$regex": "green_sub"}}}},
        { "$match": {"year" : year}},
        { "$sort": {"count": -1}},
        { "$limit": 20 }
      ]
    return list(db['Publications'].aggregate(pipeline))


def get_total_articles()->int:
    db = get_db()
    return len(list(db['Publications'].find({'doctype': 'article'})))

def get_total_preprints()->int:
    db = get_db()
    return len(list(db['Publications'].find({'doctype': 'preprint'})))