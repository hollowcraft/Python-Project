import zipfile
import os
import yaml  # pip install pyyaml
import glob

# Chemins
whitelist_path = "gamebanana/whitelist.txt"  # ton preset de mods
dependencies_txt = "gamebanana/dependencies.txt"

def get_dependencies_from_zip(zip_path):
    """Ouvre le zip et récupère les dépendances dans everest.yaml"""
    zip_name_only = os.path.splitext(os.path.basename(zip_path))[0]  # nom du zip sans extension
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            if file_name.endswith("everest.yaml"):
                content = zip_ref.read(file_name).decode("utf-8")
                data = yaml.safe_load(content)

                dependencies = []

                if isinstance(data, dict):
                    deps = data.get("Dependencies", [])
                    for dep in deps:
                        dependencies.append(dep.get("Name") + ".zip")
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and "Dependencies" in item:
                            for dep in item["Dependencies"]:
                                dependencies.append(dep.get("Name") + ".zip")

                # Ajouter le mod principal (celui téléchargé)
                dependencies.append(zip_name_only + ".zip")

                return dependencies

    # Si pas de everest.yaml trouvé, on met juste le nom du zip
    return [zip_name_only + ".zip"]

def read_whitelist(file_path):
    """Lit un fichier whitelist.txt et renvoie la liste des mods"""
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

# Trouver le premier .zip dans le dossier gamebanana/
zip_files = glob.glob(os.path.join("gamebanana", "*.zip"))
if not zip_files:
    raise FileNotFoundError("Aucun fichier .zip trouvé dans le dossier gamebanana/")
zip_path = zip_files[0]  # prend le premier zip trouvé

# 1. Récupérer les dépendances du zip
deps = get_dependencies_from_zip(zip_path)

# 2. Ajouter les mods du preset whitelist
deps += read_whitelist(whitelist_path)

# Enlever les doublons
deps = list(dict.fromkeys(deps))

# 3. Créer le dossier si nécessaire
os.makedirs("gamebanana", exist_ok=True)

# 4. Sauvegarder dans dependencies.txt
with open(dependencies_txt, "w", encoding="utf-8") as f:
    for dep_name in deps:
        f.write(dep_name + "\n")

print("Dependencies.txt créé avec le .zip et les mods du preset whitelist.")

#os.startfile("gamebanana/whitelistpy")