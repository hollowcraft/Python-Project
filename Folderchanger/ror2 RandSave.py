import json
import random

# Nom du fichier à modifier
file_path = r"C:\Users\Adam\AppData\LocalLow\Hopoo Games, LLC\Risk of Rain 2\ProperSave\Saves\a9c8ddad-e07d-422b-85eb-35f516891b33.json"

# Charger la sauvegarde JSON
with open(file_path, "r") as f:
    data = json.load(f)

# Fonction pour modifier récursivement les valeurs
def randomize_values(obj):
    if isinstance(obj, dict):
        return {k: randomize_values(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [randomize_values(v) for v in obj]
    elif isinstance(obj, bool):
        return random.choice([True, False])
    elif isinstance(obj, int):
        return obj if obj == 76561198385279682 else random.randint(0, 10000)  
    elif isinstance(obj, float):
        return round(random.uniform(0, 10000), 3)
    else:
        return obj  # Garder les autres types inchangés

# Modifier les valeurs aléatoirement (sauf la valeur spécifique)
data_randomized = randomize_values(data)

# Sauvegarder directement dans le même fichier
with open(file_path, "w") as f:
    json.dump(data_randomized, f, indent=4)

print(f"La sauvegarde '{file_path}' a été modifiée avec des valeurs aléatoires (sauf 76561198385279682).")
