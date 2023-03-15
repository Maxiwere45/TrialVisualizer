import requests
import json

# URL de base pour l'API CrossRef
base_url = "https://api.crossref.org/works/"

def get_doi(url_doi: str) -> str:
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


