import csv
import ast
import pymongo
from datetime import datetime
from pymongo import MongoClient

## CONNEXION A LA BASE DE DONNEES
client = MongoClient('mongodb+srv://nrm4206a:9dfe351b@dbsae.ohuhcxc.mongodb.net/?retryWrites=true&w=majority')

# Connection à la base de données MongoDB
db = client['trial_visualizer']
ClinicalTrials = db['ClinicalTrials']
Publications = db['Publications']


## EXTRACTION DES DONNEES DES FICHIERS CSV ET TRANSFORMATION
# ESSAIS CLINIQUE
def traitement_CSV_IMPORT(csv_type: str, csv_file):
    lecteur_csv = csv.DictReader(csv_file)
    dataPython = [dict(ligne) for ligne in lecteur_csv]
    for i in range(len(dataPython)):
        if csv_type == 'Clinical trial obstudies':
            # Conversion de la chaine de caractère sur [interventions] en liste de dictionnaires
            interventions_string = dataPython[i]['interventions']
            if len(interventions_string) > 0:
                interventions = ast.literal_eval(interventions_string)
                dataPython[i]['interventions'] = interventions

            # Conversion de la chaine de caractère sur [conditions] en liste de string
            data_conditions = dataPython[i]['conditions']
            if len(data_conditions) > 0:
                data_list = [data.strip() for data in data_conditions.split('•')]
                dataPython[i]['conditions'] = data_list

            # Autres modifications
            dataPython[i]['trial_type'] = "cl_obstudies"
            dateP = datetime.strptime(dataPython[i]['dateInserted'], '%m/%d/%Y').date()
            dataPython[i]['dateInserted'] = dateP.strftime('%Y-%m-%d')
            if len(dataPython[i]['date']) > 0:
                dateF = datetime.strptime(dataPython[i]['date'], '%m/%d/%Y').date()
                dataPython[i]['date'] = dateF.strftime('%Y-%m-%d')
        elif csv_type == 'Clinical trial randtrial':
            interventions_string = dataPython[i]['interventions']
            if len(interventions_string) > 0:
                interventions = ast.literal_eval(interventions_string)
                dataPython[i]['interventions'] = interventions

            data_conditions = dataPython[i]['conditions']
            if len(data_conditions) > 0:
                data_list = [data.strip() for data in data_conditions.split('•')]
                dataPython[i]['conditions'] = data_list

            # Autres modifications
            dataPython[i]['trial_type'] = "cl_randtrials"
            try:
                if len(dataPython[i]['dateInserted']) > 0:
                    dateP = datetime.strptime(dataPython[i]['dateInserted'], '%m/%d/%Y').date()
                    dataPython[i]['dateInserted'] = dateP.strftime('%Y-%m-%d')
                if len(dataPython[i]['date']) > 0:
                    dateF = datetime.strptime(dataPython[i]['date'], '%m/%d/%Y').date()
                    dataPython[i]['date'] = dateF.strftime('%Y-%m-%d')
            except ValueError:
                continue
        elif csv_type == 'Publications randtrial':
            openAccess = dataPython[i]['openAccess']
            if len(openAccess) > 0:
                data_list = [data.strip() for data in openAccess.split('•')]
                dataPython[i]['openAccess'] = data_list

            concepts = dataPython[i]['concepts']
            if len(concepts) > 0:
                data_list = [data.strip() for data in concepts.split('•')]
                dataPython[i]['concepts'] = data_list

            meshTerms = dataPython[i]['meshTerms']
            if len(meshTerms) > 0:
                data_list = [data.strip() for data in meshTerms.split('•')]
                dataPython[i]['meshTerms'] = data_list

            # Autres modifications
            dataPython[i]['authors'] = "N/A"
            dataPython[i]['p_type'] = "p_randtrials"

            try:
                dataPython[i]['year'] = int(dataPython[i]['year'])
                if len(dataPython[i]['dateInserted']) > 0:
                    dateP = datetime.strptime(dataPython[i]['dateInserted'], '%m/%d/%Y').date()
                    dataPython[i]['dateInserted'] = dateP.strftime('%Y-%m-%d')

                if len(dataPython[i]['datePublished']) > 0:
                    dateF = datetime.strptime(dataPython[i]['datePublished'], '%m/%d/%Y').date()
                    dataPython[i]['datePublished'] = dateF.strftime('%Y-%m-%d')
            except ValueError:
                continue
        elif csv_type == 'Publications obstudies':
            openAccess = dataPython[i]['openAccess']
            if len(openAccess) > 0:
                data_list = [data.strip() for data in openAccess.split('•')]
                dataPython[i]['openAccess'] = data_list

            concepts = dataPython[i]['concepts']
            if len(concepts) > 0:
                data_list = [data.strip() for data in concepts.split('•')]
                dataPython[i]['concepts'] = data_list

            meshTerms = dataPython[i]['meshTerms']
            if len(meshTerms) > 0:
                data_list = [data.strip() for data in meshTerms.split('•')]
                dataPython[i]['meshTerms'] = data_list

            # Autres modifications
            dataPython[i]['authors'] = "N/A"
            dataPython[i]['p_type'] = "p_obstudies"
            dataPython[i]['year'] = int(dataPython[i]['year'])
            try:
                if len(dataPython[i]['dateInserted']) > 0:
                    dateP = datetime.strptime(dataPython[i]['dateInserted'], '%m/%d/%Y').date()
                    dataPython[i]['dateInserted'] = dateP.strftime('%Y-%m-%d')

                if len(dataPython[i]['datePublished']) > 0:
                    dateF = datetime.strptime(dataPython[i]['datePublished'], '%m/%d/%Y').date()
                    dataPython[i]['datePublished'] = dateF.strftime('%Y-%m-%d')
            except ValueError:
                continue

# Insérer les données dans la base de données
print("Insertion des données dans la base de données...")

# NE PAS DE-COMMENTER, LES DONNES SONT DEJA INSERE
"""
ClinicalTrials.insert_many(c_trial_obstudies) # SUCCESS
ClinicalTrials.insert_many(c_trial_randtrials) # SUCCESS
"""
Publications.insert_many(pub_obstudies)  # SUCCESS
Publications.insert_many(pub_randtrials)  # SUCCESS

print("Insertion des données terminée !")
print("\t> Nombre de ClinicalTrials : ", ClinicalTrials.count_documents({}))
print("\t> Nombre de publications : ", Publications.count_documents({}))

# Fermeture de la connexion à la base de données
connect.client.close()
