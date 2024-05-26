import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# URL du site
url = "https://offsetcode.com/themes/messenger/2.2.0/"

# Répertoire de destination pour enregistrer les fichiers
destination_folder = "site_social_webestica"

# Fonction pour télécharger le contenu de l'URL
def download_content(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        # Créer le dossier parent s'il n'existe pas
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        # Vérifier si le fichier existe déjà
        if not os.path.exists(filename):
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Téléchargement de {filename} terminé avec succès.")
        else:
            print(f"{filename} existe déjà, le téléchargement est ignoré.")
    else:
        print(f"Échec du téléchargement de {filename}.")

# Fonction pour extraire et télécharger les ressources d'une page HTML
def download_resources(html, page_url):
    soup = BeautifulSoup(html, 'html.parser')
    # Récupérer tous les liens vers les ressources
    links = soup.find_all(['link', 'script', 'img', 'a'])
    for link in links:
        if link.name == 'link' and link.get('rel') == ['stylesheet']:
            resource_url = link.get('href')
        else:
            resource_url = link.get('src') or link.get('href')
        if resource_url and not resource_url.startswith('javascript:'):
            # Construire l'URL absolue si nécessaire
            absolute_url = urljoin(page_url, resource_url)
            # Extraire le chemin relatif du fichier
            relative_path = urlparse(absolute_url).path.lstrip('/')
            # Télécharger la ressource
            download_content(absolute_url, os.path.join(destination_folder, relative_path))

# Fonction pour télécharger une page HTML et ses ressources
def download_page(url):
    # Télécharger la page HTML
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        # Enregistrer la page HTML
        with open(os.path.join(destination_folder, "index.html"), 'w', encoding='utf-8') as f:
            f.write(html)
        print("Téléchargement de la page index.html terminé avec succès.")
        # Télécharger les ressources
        download_resources(html, url)
    else:
        print("Échec du téléchargement de la page index.html.")

# Créer le répertoire de destination s'il n'existe pas
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Télécharger la page principale et ses ressources
download_page(url)

print("Téléchargement complet.")

