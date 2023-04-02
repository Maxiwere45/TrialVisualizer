import pymongo

MONGO_URI = 'mongodb+srv://nrm4206a:9dfe351b@dbsae.ohuhcxc.mongodb.net/?retryWrites=true&w=majority'
client = pymongo.MongoClient(MONGO_URI)
db = client['trial_visualizer']
clinicaltrials = db['ClinicalTrials']
publications = db['Publications']

"""
val1 = list(publications.find({'authors':'N/A'},{'_id':0,'id':1,'doi':1}))
print("Ajout des auteurs aux publications...")
print("Nombre de publications à traiter : " + str(len(val1)))
print("Ceci peut prendre quelques minutes...")
x = len(val1)
for i in val1:
    metadata = DOI_SEARCH.get_doi(i['doi'])
    authors = []
    if 'author' in metadata:
        for author in metadata['author']:
            if 'family' in author and 'given' not in author:
                name = author['family']
            elif 'given' in author and 'family' not in author:
                name = author['given']
            elif 'given' in author and 'family' in author:
                name = author['given'] + ' ' + author['family']
            else:
                name = 'Unknown'
            authors.append(name)
        r = publications.update_one({'id':i['id']},{'$set':{'authors':authors}})
        x -= 1
        print("Il reste " + str(x) + " publications à traiter...")
print("Traitement terminé !")
"""

def aggregate_to_dict(query):
    cursor = db.Publications.aggregate(query)
    result = []
    for doc in cursor:
        id_value = doc['_id']['venue']
        count_value = doc['count']
        result.append({'id': id_value, 'count': count_value})
    return result

query = [
  {
    '$group': {
      '_id': {
        'venue': '$venue'
      },
      'count': {
        '$sum': 1
      }
    }
  },
  {
    '$sort': {
      '_id.year': 1,
      'count': -1
    }
  }
]

result = aggregate_to_dict(query)
print(result)

