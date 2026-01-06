import json
import os
import glob

# 📂 Dossier contenant les saves JSON
save_folder = r"C:\Users\Adam\AppData\LocalLow\Hopoo Games, LLC\Risk of Rain 2\ProperSave\Saves\bqckup\solo"

# 📜 Charger toutes les saves du dossier
save_files = glob.glob(os.path.join(save_folder, "*.json"))

if len(save_files) < 2:
    print("❌ Il faut au moins 2 fichiers JSON pour comparer !")
    exit()

# 🔍 Charger toutes les saves
saves = []
for file in save_files:
    with open(file, "r") as f:
        saves.append(json.load(f))

# 🔄 Fonction récursive pour comparer les valeurs
def find_common_values(*dicts):
    if not dicts:
        return {}

    # Prendre la première save comme référence
    reference = dicts[0]

    if isinstance(reference, dict):
        # Vérifier chaque clé présente dans toutes les saves
        common = {
            k: find_common_values(*[d[k] for d in dicts if k in d])
            for k in reference if all(k in d for d in dicts)
        }
        return {k: v for k, v in common.items() if v != {}}

    elif isinstance(reference, list):
        # Vérifier si toutes les listes sont identiques
        if all(d == reference for d in dicts):
            return reference
        return []

    else:
        # Vérifier si la valeur est identique dans toutes les saves
        if all(d == reference for d in dicts):
            return reference
        return None

# 📊 Trouver les valeurs identiques dans toutes les saves
common_values = find_common_values(*saves)

# 📁 Sauvegarder le résultat dans un fichier
output_file = r"C:\Users\Adam\AppData\LocalLow\Hopoo Games, LLC\Risk of Rain 2\ProperSave\Saves\common_values.json"
with open(output_file, "w") as f:
    json.dump(common_values, f, indent=4)
print(common_values)
print(f"✅ Analyse terminée ! Les valeurs communes sont enregistrées dans '{output_file}'.")
