import re
import requests
import json
import os
import shutil
import glob

# Chemins
celeste_mods_dir = r"C:\Program Files (x86)\Steam\steamapps\common\Celeste\Mods"
local_dir = "gamebanana"

def get_allowed_fields(item_type="Mod"):
    url = f"http://api.gamebanana.com/Core/Item/Data/AllowedFields?itemtype={item_type}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def download_first_zip(mod_url):
    # Extraire l'ID du mod
    match = re.search(r'/mods/(\d+)', mod_url)
    if not match:
        raise ValueError("URL invalide")
    mod_id = match.group(1)

    # Récupérer les champs valides
    fields = get_allowed_fields("Mod")

    # Récupérer les données du mod
    api_url = "http://api.gamebanana.com/Core/Item/Data"
    params = {
        "itemtype": "Mod",
        "itemid": mod_id,
        "fields": ",".join(fields)
    }
    response = requests.get(api_url, params=params)
    response.raise_for_status()
    print(response)
    data = response.json()

    # Sauvegarder le JSON complet localement
    os.makedirs(local_dir, exist_ok=True)
    with open(os.path.join(local_dir, "response.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # Chercher les fichiers dans le JSON
    files_dict = None
    for entry in data:
        if isinstance(entry, dict) and all(isinstance(v, dict) for v in entry.values()):
            files_dict = entry
            break

    if not files_dict:
        print("Aucun fichier trouvé pour ce mod.")
        return None

    # Télécharger le premier .zip trouvé
    for file_id, file_data in files_dict.items():
        if isinstance(file_data, dict) and file_data.get("_sFile", "").endswith(".zip"):
            zip_url = file_data["_sDownloadUrl"]
            zip_name = file_data["_sFile"]

            # Chemins de destination
            local_zip_path = os.path.join(local_dir, zip_name)
            celeste_zip_path = os.path.join(celeste_mods_dir, zip_name)

            # Créer les dossiers si nécessaire
            os.makedirs(local_dir, exist_ok=True)
            os.makedirs(celeste_mods_dir, exist_ok=True)

            # Télécharger et enregistrer dans gamebanana/
            r = requests.get(zip_url)
            r.raise_for_status()
            with open(local_zip_path, "wb") as f_zip:
                f_zip.write(r.content)

            # Copier vers Celeste/Mods
            shutil.copy(local_zip_path, celeste_zip_path)

            print(f"Mod téléchargé dans : {local_zip_path}")
            print(f"Mod installé dans : {celeste_zip_path}")
            return local_zip_path

    print("Aucun .zip trouvé pour ce mod.")
    return None


# Exemple d'utilisation
zip_files = glob.glob(os.path.join("gamebanana", "*.zip"))
if zip_files:
    os.remove(zip_files[0])

with open("extention/url.txt", "r", encoding="utf-8") as fichier:
    mod_url = fichier.read()
zip_file = download_first_zip(mod_url)
