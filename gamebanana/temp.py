import os

# Chemins
dependencies_file = "gamebanana/dependencies.txt"
blacklist_file = r"C:\Program Files (x86)\Steam\steamapps\common\Celeste\Mods\blacklist.txt"  # adapte le chemin selon ton installation

# Lire les dépendances
with open(dependencies_file, "r", encoding="utf-8") as f:
    deps = set(line.strip() for line in f if line.strip())

# Lire le blacklist.txt
with open(blacklist_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Modifier les lignes pour whitelister les dépendances
new_lines = []
for line in lines:
    stripped = line.strip()
    if not stripped or stripped.startswith("#") is False:
        # Ligne vide ou déjà whitelisted
        new_lines.append(line)
        continue

    mod_name = stripped.lstrip("#").strip()
    if mod_name in deps:
        # Enlever le '#' pour whitelister
        new_lines.append(mod_name + "\n")
    else:
        new_lines.append(line)

# Écrire le blacklist modifié
with open(blacklist_file, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Blacklist mise à jour : dépendances whitelisted")
