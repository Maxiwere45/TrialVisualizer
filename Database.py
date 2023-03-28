import pymongo
from flask import g

class Database:
    MONGO_URI = 'mongodb+srv://nrm4206a:9dfe351b@dbsae.ohuhcxc.mongodb.net/?retryWrites=true&w=majority'
    def __init__(self):
        self.uri = self.MONGO_URI

    def get_db(self):
        if 'db' not in g:
            client = pymongo.MongoClient(self.uri)
            g.db = client['trial_visualizer']
        return g.db

    def get_trial(self):
        db = self.get_db()
        return list(db['ClinicalTrials'].find().limit(1300))

    def get_trial_obstudies(self):
        db = self.get_db()
        return list(db['ClinicalTrials'].find({'trial_type': 'cl_obstudies'}).limit(1300))

    def get_trial_randtrials(self):
        db = self.get_db()
        return list(db['ClinicalTrials'].find({'trial_type': 'cl_randtrials'}).limit(1300))

    def get_publication(self):
        db = self.get_db()
        return list(db['Publications'].find().limit(1300))

    def get_publication_obstudies(self):
        db = self.get_db()
        return list(db['Publications'].find({'p_type': 'p_obstudies'}).limit(1300))

    def get_publication_randtrials(self):
        db = self.get_db()
        return list(db['Publications'].find({'p_type': 'p_randtrials'}).limit(1300))

    # Nombre d'essais en phase 1 / 2 / 3 / 4
    def get_phase_by_nb(self):
        db = self.get_db()
        return list(db['ClinicalTrials'].aggregate([
            {
                "$group": {
                    "_id": "$phase",
                    "count": {
                        "$sum": 1
                    }
                }
            },
            { "$sort": { "count": -1 } }
        ]))

    @staticmethod
    def close_db(e=None):
        db = g.pop('db', None)
        if db is not None:
            db.client.close()

    def init_app(self, app):
        app.teardown_appcontext(self.close_db)

    def get_total_essais(self):
        db = self.get_db()
        return len(list(db['ClinicalTrials'].find()))

    def get_total_esais_fem(self):
        db = self.get_db()
        return len(list(db['ClinicalTrials'].find({'gender': 'Female'})))

    def get_total_esais_male(self):
        db = self.get_db()
        return len(list(db['ClinicalTrials'].find({'gender':'Male'})))

    def get_total_pub(self):
        db = self.get_db()
        return db['ClinicalTrials'].count_documents({'$and':[{'p_type':'p_obstudies'},{'p_type':'p_randtrials'}]})
