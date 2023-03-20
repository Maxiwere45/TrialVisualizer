import csv
import ast
import pymongo
import connect
from datetime import datetime

# Connection à la base de données MongoDB
db = connect.client['trial_visualizer']
ClinicalTrials = db['ClinicalTrials']
Publications = db['Publications']

## EXTRACTION DES DONNEES DES FICHIERS CSV ET TRANSFORMATION
# ESSAIS CLINIQUE
with open('./data_extracted/C_obstudies.csv', 'r') as f:
    lecteur_csv = csv.DictReader(f)
    c_trial_obstudies = [dict(ligne) for ligne in lecteur_csv]
    for i in range(len(c_trial_obstudies)):
        # Conversion de la chaine de caractère sur [interventions] en liste de dictionnaires
        interventions_string = c_trial_obstudies[i]['interventions']
        if len(interventions_string) > 0:
            interventions = ast.literal_eval(interventions_string)
            c_trial_obstudies[i]['interventions'] = interventions

        # Conversion de la chaine de caractère sur [conditions] en liste de string
        data_conditions = c_trial_obstudies[i]['conditions']
        if len(data_conditions) > 0:
            data_list = [data.strip() for data in data_conditions.split('•')]
            c_trial_obstudies[i]['conditions'] = data_list

        # Autres modifications
        c_trial_obstudies[i]['trial_type'] = "cl_obstudies"
        dateP = datetime.strptime(c_trial_obstudies[i]['dateInserted'], '%m/%d/%Y').date()
        c_trial_obstudies[i]['dateInserted'] = dateP.strftime('%Y-%m-%d')
        if len(c_trial_obstudies[i]['date']) > 0:
            dateF = datetime.strptime(c_trial_obstudies[i]['date'], '%m/%d/%Y').date()
            c_trial_obstudies[i]['date'] = dateF.strftime('%Y-%m-%d')

with open('./data_extracted/C_randTrials.csv', 'r') as f:
    lecteur_csv = csv.DictReader(f)
    c_trial_randtrials = [dict(ligne) for ligne in lecteur_csv]
    for i in range(len(c_trial_randtrials)):
        interventions_string = c_trial_randtrials[i]['interventions']
        if len(interventions_string) > 0:
            interventions = ast.literal_eval(interventions_string)
            c_trial_randtrials[i]['interventions'] = interventions

        data_conditions = c_trial_randtrials[i]['conditions']
        if len(data_conditions) > 0:
            data_list = [data.strip() for data in data_conditions.split('•')]
            c_trial_randtrials[i]['conditions'] = data_list

        # Autres modifications
        c_trial_randtrials[i]['trial_type'] = "cl_randtrials"
        try:
            if len(c_trial_randtrials[i]['dateInserted']) > 0:
                dateP = datetime.strptime(c_trial_randtrials[i]['dateInserted'], '%m/%d/%Y').date()
                c_trial_randtrials[i]['dateInserted'] = dateP.strftime('%Y-%m-%d')
            if len(c_trial_randtrials[i]['date']) > 0:
                dateF = datetime.strptime(c_trial_randtrials[i]['date'], '%m/%d/%Y').date()
                c_trial_randtrials[i]['date'] = dateF.strftime('%Y-%m-%d')
        except ValueError:
            continue

# PUBBLICATIONS
with open('./data_extracted/P_obstudies.csv', 'r') as f:
    lecteur_csv = csv.DictReader(f)
    pub_obstudies = [dict(ligne) for ligne in lecteur_csv]
    for i in range(len(pub_obstudies)):
        openAccess = pub_obstudies[i]['openAccess']
        if len(openAccess) > 0:
            data_list = [data.strip() for data in openAccess.split('•')]
            pub_obstudies[i]['openAccess'] = data_list

        concepts = pub_obstudies[i]['concepts']
        if len(concepts) > 0:
            data_list = [data.strip() for data in concepts.split('•')]
            pub_obstudies[i]['concepts'] = data_list

        meshTerms = pub_obstudies[i]['meshTerms']
        if len(meshTerms) > 0:
            data_list = [data.strip() for data in meshTerms.split('•')]
            pub_obstudies[i]['meshTerms'] = data_list

        # Autres modifications
        pub_obstudies[i]['authors'] = "N/A"
        pub_obstudies[i]['p_type'] = "p_obstudies"
        pub_obstudies[i]['year'] = int(pub_obstudies[i]['year'])
        try:
            if len(pub_obstudies[i]['dateInserted']) > 0:
                dateP = datetime.strptime(pub_obstudies[i]['dateInserted'], '%m/%d/%Y').date()
                pub_obstudies[i]['dateInserted'] = dateP.strftime('%Y-%m-%d')

            if len(pub_obstudies[i]['datePublished']) > 0:
                dateF = datetime.strptime(pub_obstudies[i]['datePublished'], '%m/%d/%Y').date()
                pub_obstudies[i]['datePublished'] = dateF.strftime('%Y-%m-%d')
        except ValueError:
            continue

with open('./data_extracted/P_randTrials.csv', 'r') as f:
    lecteur_csv = csv.DictReader(f)
    pub_randtrials = [dict(ligne) for ligne in lecteur_csv]
    for i in range(len(pub_randtrials)):
        openAccess = pub_randtrials[i]['openAccess']
        if len(openAccess) > 0:
            data_list = [data.strip() for data in openAccess.split('•')]
            pub_randtrials[i]['openAccess'] = data_list

        concepts = pub_randtrials[i]['concepts']
        if len(concepts) > 0:
            data_list = [data.strip() for data in concepts.split('•')]
            pub_randtrials[i]['concepts'] = data_list

        meshTerms = pub_randtrials[i]['meshTerms']
        if len(meshTerms) > 0:
            data_list = [data.strip() for data in meshTerms.split('•')]
            pub_randtrials[i]['meshTerms'] = data_list

        # Autres modifications
        pub_randtrials[i]['authors'] = "N/A"
        pub_randtrials[i]['p_type'] = "p_randtrials"

        try:
            pub_randtrials[i]['year'] = int(pub_randtrials[i]['year'])
            if len(pub_randtrials[i]['dateInserted']) > 0:
                dateP = datetime.strptime(pub_randtrials[i]['dateInserted'], '%m/%d/%Y').date()
                pub_randtrials[i]['dateInserted'] = dateP.strftime('%Y-%m-%d')

            if len(pub_randtrials[i]['datePublished']) > 0:
                dateF = datetime.strptime(pub_randtrials[i]['datePublished'], '%m/%d/%Y').date()
                pub_randtrials[i]['datePublished'] = dateF.strftime('%Y-%m-%d')
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
