import os

# Chemins
dependencies_file = "gamebanana/dependencies.txt"
blacklist_file = r"C:\Program Files (x86)\Steam\steamapps\common\Celeste\Mods\blacklist.txt"

# Lire les dépendances
with open(dependencies_file, "r", encoding="utf-8") as f:
    deps = set(line.strip() for line in f if line.strip())

# Lire le blacklist.txt
with open(blacklist_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Processer le reste des lignes
body_lines = lines[3:]  # à partir de la 4ème ligne
new_body = []

for line in body_lines:
    mod_name = line.strip().lstrip("#").strip()
    if not mod_name:
        new_body.append(line)
        continue
    # Ajouter # seulement si le mod est dans les dépendances
    if mod_name in deps:
        new_body.append(f"# {mod_name}\n")
    else:
        new_body.append(f"{mod_name}\n")  # enlever le # pour les autres

# Écrire le blacklist final
with open(blacklist_file, "w", encoding="utf-8") as f:
    f.writelines(new_body)

print("Blacklist mise à jour avec les mods de dependencies.txt whitelisted.")
