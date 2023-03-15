import pymongo

MONGO_URI = 'mongodb+srv://nrm4206a:9dfe351b@dbsae.ohuhcxc.mongodb.net/?retryWrites=true&w=majority'
client = pymongo.MongoClient(MONGO_URI)
db = client['trial_visualizer']
clinicaltrials = db['ClinicalTrials']
publications = db['Publications']

# Nombre d'essais en phase 1 / 2 / 3 / 4
val = clinicaltrials.aggregate([{
        "$group": {
            "_id": "$phase",
            "count": {
                "$sum": 1
            }
        }
}])

print(list(val))
