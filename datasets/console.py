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

# Nombre d'essais en phase 1 / 2 / 3 / 4

print(len(list(db['ClinicalTrials'].find({'gender':'Male'}))))
