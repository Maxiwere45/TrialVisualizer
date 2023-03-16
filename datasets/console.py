import json
import pymongo
import script_doi_extract as DOI_SEARCH

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

# Nombre d'essais en phase 1 / 2 / 3 / 4
val = clinicaltrials.aggregate([{
        "$group": {
            "_id": "$phase",
            "count": {
                "$sum": 1
            }
        }
}])

result = list(val)

print(result)


# [{'_id': 'Retrospective study', 'count': 21},
#  {'_id': 'Phase 0', 'count': 90},
#  {'_id': 'New Treatment Measure Clinical Study', 'count': 1},
#  {'_id': 'N/A', 'count': 996},
#  {'_id': '', 'count': 64},
#  {'_id': 'Phase 3', 'count': 389},
#  {'_id': 'Phase 1/2', 'count': 85},
#  {'_id': 'Phase 4', 'count': 155},
#  {'_id': 'Phase 2', 'count': 430},
#  {'_id': 'Phase 1', 'count': 90},
#  {'_id': 'Phase 2/3', 'count': 139}]

"""
Voici une liste contenant des dictionnaires : [{'_id': 'Retrospective study', 'count': 21}, {'_id': 'Phase 0', 'count': 81}, {'_id': 'New Treatment Measure Clinical Study', 'count': 1}, {'_id': '2', 'count': 1}, {'_id': '4', 'count': 3}, {'_id': 'N/A', 'count': 996}, {'_id': '', 'count': 64}, {'_id': 'Phase 3', 'count': 389}, {'_id': 'Phase 1/2', 'count': 85}, {'_id': 'Phase 4', 'count': 152}, {'_id': 'Phase 2', 'count': 429}, {'_id': '0', 'count': 8}, {'_id': 'Phase 1', 'count': 90}, {'_id': 'Phase 2/3', 'count': 139}] 
Comme tu peux le remarquer, certaines colonnes de '_id' sont similaires (ex. 'Phase 2' et '2'). écris un script python qui va fusionner les doublons en renommant les valeurs des '_id' (ex. 'Phase 2' et '2' -> 'Phase 2') et en fusionnant leurs colonne 'counts'. Le résultat attendu devrai être de cette forme
 : 
"""