import requests
import json

# URL de base pour l'API CrossRef
base_url = "https://api.crossref.org/works/"

# DOI à rechercher
doi = "10.1101/2020.05.24.20111823"


def get_doi(url_doi: str):
    # Construire l'URL pour la requête CrossRef
    url = base_url + url_doi

    # Effectuer la requête CrossRef
    response = requests.get(url)

    # Extraire les informations de réponse JSON
    try:
        if response.status_code == 200:
            data = json.loads(response.text)['message']
            return data
        else:
            return f"Erreur {response.status_code} lors de la requête CrossRef."
    except IndexError:
        return "DOI non trouvé."
