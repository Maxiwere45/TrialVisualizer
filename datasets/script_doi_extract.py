import requests
import json

# URL de base pour l'API CrossRef
base_url = "https://api.crossref.org/works/"

# DOI à rechercher
doi = "10.1101/2020.05.24.20111823"

# Construire l'URL pour la requête CrossRef
url = base_url + doi

# Effectuer la requête CrossRef
response = requests.get(url)

# Extraire les informations de réponse JSON
try:
    if response.status_code == 200:
        data = json.loads(response.text)['message']
        title = data['title'][0]
        print(data)
        """
        authors = ", ".join(author['given'] + " " + author['family'] for author in data['author'])
        journal = data['container-title'][0]
        date = data['issued']['date-parts'][0]
        print(f"Titre: {title}")
        print(f"Auteurs: {authors}")
        print(f"Journal: {journal}")
        print(f"Date de publication: {'/'.join(str(d) for d in date)}")
        """
    else:
        print(f"Erreur {response.status_code} lors de la requête CrossRef.")
except IndexError:
    print("DOI non trouvé.")


