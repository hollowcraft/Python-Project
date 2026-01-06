import requests
import os

url = "https://gamebanana.com/mods/498912"

response = requests.get(url)
script_dir = os.path.dirname(os.path.abspath(__file__))

if response.status_code == 200:
    content_type = response.headers.get('Content-Type', '')
    # Détermine l'extension selon le type de contenu
    if 'html' in content_type:
        filename = "page.html"
        mode = "w"
        data = response.text
        encoding = "utf-8"
    elif 'zip' in content_type or 'octet-stream' in content_type:
        filename = "fichier.zip"
        mode = "wb"
        data = response.content
        encoding = None
    else:
        filename = "fichier_binaire"
        mode = "wb"
        data = response.content
        encoding = None

    output_path = os.path.join(script_dir, filename)
    if "b" in mode:
        with open(output_path, mode) as file:
            file.write(data)
    else:
        with open(output_path, mode, encoding=encoding) as file:
            file.write(data)
    print(f"Le fichier {filename} a été créé avec succès à l'emplacement : {output_path}")
else:
    print(f"Erreur lors de la récupération de la page : {response.status_code}")
