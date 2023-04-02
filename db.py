from datetime import datetime, timedelta

import pymongo
from bson import SON
from flask import g

from datasets.console import db

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


def get_trial_id(id_trial: str):
    db = get_db()
    result = list(db['ClinicalTrials'].find({'id': id_trial}))
    return dict(result[0])


def get_total_pub():
    db = get_db()
    return len(list(db['Publications'].find({})))


def get_total_pub_essais_rand():
    db = get_db()
    return db['Publications'].count_documents({'p_type': 'p_randtrials'})


def get_total_pub_essais_obs():
    db = get_db()
    return db['Publications'].count_documents({'p_type': 'p_obstudies'})


def get_pub_id(id_pub: str):
    db = get_db()
    result = list(db['Publications'].find({'id': id_pub}))
    return dict(result[0])


def get_top_concepts_by_publication_count(year:str):
    db = get_db()
    pipeline = [
        {"$match": {"doctype": "article"}},
        {"$unwind": "$concepts"},
        {"$group": {"_id": "$concepts", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$match": {"year": year}}
    ]
    return list(db['Publications'].aggregate(pipeline))[0:20]


def get_total_articles() -> int:
    db = get_db()
    return len(list(db['Publications'].find({'doctype': 'article'})))


def get_total_preprints() -> int:
    db = get_db()
    return len(list(db['Publications'].find({'doctype': 'preprint'})))


# STATISTIQUES ESSAIS CLINIQUES
def get_gender_stats():
    db = get_db()
    return list(db.ClinicalTrials.aggregate([
        {"$group":
             {"_id": "$gender",
              "count": {"$sum": 1}
              }
         }
    ]))


# STATISTIQUES PUBLICATIONS
def get_revue_abs():
    db = get_db()
    pipeline = [
        {
            "$group": {
                "_id": {
                    "venue": "$venue",
                    "year": {"$year": "$datePublished"}
                },
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": SON([("_id.year", 1), ("count", -1)])
        }
    ]
    return db['Publications'].aggregate(pipeline, allowDiskUse=True)

def get_current_month_publications():
  current_date = datetime.utcnow()
  start_of_month = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
  end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)
  query = {
    "datePublished": {
      "$gte": start_of_month,
      "$lte": end_of_month
    }
  }
  sort = [("altmetric", -1), ("timesCited", -1)]
  return list(db.Publications.find(query).sort(sort))