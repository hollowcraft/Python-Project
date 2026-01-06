import json

# Chemins des fichiers
save_file = r"C:\Users\Adam\AppData\LocalLow\Hopoo Games, LLC\Risk of Rain 2\ProperSave\Saves\9bd28171-08b2-473c-bd8e-0df603743fef.json"
data_file = "web/ror2save/data.json"

# Charger la save originale
with open(save_file, "r", encoding="utf-8") as f:
    save_content = json.load(f)

# Charger les données à injecter
with open(data_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Modifier les valeurs de la save originale avec celles de data.json
save_content["r"]["d"] = data["difficulty"]
save_content["r"]["sn"] = data["map"]

save_content["p"][0]["m"]["bn"] = data["player1"]["perso"]
# Mettre à jour les items de player1
save_content["p"][0]["m"]["i"]["i"] = [{"i": item[0], "c": item[1]} for item in data["player1"]["items"]]

save_content["p"][1]["m"]["bn"] = data["player2"]["perso"]
# Mettre à jour les items de player2
save_content["p"][1]["m"]["i"]["i"] = [{"i": item[0], "c": item[1]} for item in data["player2"]["items"]]

# Écrire la save modifiée
with open(save_file, "w", encoding="utf-8") as f:
    json.dump(save_content, f, ensure_ascii=False, indent=4)

print("Save mise à jour avec les données de data.json !")
