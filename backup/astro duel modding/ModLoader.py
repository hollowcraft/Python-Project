import os
import shutil
import hashlib
import subprocess

# Dossier du jeu et des mods
game_directory = "C:\Program Files (x86)\Steam\steamapps\common\AstroDuel2"
mods_directory = os.path.join(game_directory, "mods")
backup_directory = os.path.join(mods_directory, "backup")

# Dossiers où les niveaux sont stockés
levels_directory = os.path.join(game_directory, "res\\levels")
sprites_directory = os.path.join(game_directory, "res\\sprites")
sfx_directory = os.path.join(game_directory, "res\\sfx")

# Fonction pour sauvegarder les fichiers du jeu dans le dossier backup
def backup_game_files():
    if not os.path.exists(backup_directory):
        print("Sauvegarde du jeu dans le dossier mods/backup...")
        os.makedirs(backup_directory)
        # Sauvegarde des fichiers de niveaux
        shutil.copytree(levels_directory, os.path.join(backup_directory, "levels"))
        # Sauvegarde des fichiers de textures
        shutil.copytree(sprites_directory, os.path.join(backup_directory, "sprites"))
        # Sauvegarde des fichiers audio
        shutil.copytree(sfx_directory, os.path.join(backup_directory, "sfx"))
        # Sauvegarde des DLL, s'ils existent
        shutil.copytree(os.path.join(game_directory, "game_dlls"), os.path.join(backup_directory, "game_dlls"))
    else:
        print("La sauvegarde existe déjà, aucune nouvelle sauvegarde effectuée.")

# Fonction pour comparer deux fichiers et retourner un hash
def get_file_hash(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

# Fonction pour appliquer un mod (y compris niveaux, DLL, textures, sons, etc.)
def apply_mod(mod_path):
    if os.path.isdir(mod_path):
        for item in os.listdir(mod_path):
            item_path = os.path.join(mod_path, item)
            if item.endswith(".dll"):
                print(f"Chargement de la DLL: {item}")
                shutil.copy(item_path, os.path.join(game_directory, "game_dlls"))
            elif item.endswith(".pvr.ccz"):
                print(f"Remplacement de la texture: {item}")
                shutil.copy(item_path, sprites_directory)
            elif item.endswith(".wav"):
                print(f"Ajout du son: {item}")
                shutil.copy(item_path, sfx_directory)
            elif item == "levels":
                apply_levels(item_path)

# Fonction pour appliquer les niveaux (remplace les niveaux du jeu)
def apply_levels(levels_path):
    for level_folder in os.listdir(levels_path):
        level_folder_path = os.path.join(levels_path, level_folder)
        if os.path.isdir(level_folder_path):
            # Vérifie si le dossier de niveaux existe déjà dans le jeu
            game_level_folder = os.path.join(levels_directory, level_folder)
            if os.path.exists(game_level_folder):
                # Vérifie les fichiers de niveau un par un
                for level_file in os.listdir(level_folder_path):
                    level_file_path = os.path.join(level_folder_path, level_file)
                    game_level_file_path = os.path.join(game_level_folder, level_file)
                    if os.path.exists(game_level_file_path):
                        # Si les fichiers sont différents, on les remplace
                        if get_file_hash(level_file_path) != get_file_hash(game_level_file_path):
                            print(f"Remplacement du niveau: {level_file}")
                            shutil.copy(level_file_path, game_level_file_path)
                    else:
                        print(f"Ajout du niveau: {level_file}")
                        shutil.copy(level_file_path, game_level_file_path)
            else:
                # Si le dossier du niveau n'existe pas, on le copie entièrement
                print(f"Ajout du dossier de niveau: {level_folder}")
                shutil.copytree(level_folder_path, game_level_folder)

# Fonction pour charger tous les mods
def load_all_mods():
    for mod_folder in os.listdir(mods_directory):
        mod_path = os.path.join(mods_directory, mod_folder)
        if os.path.isdir(mod_path):
            print(f"Application du mod: {mod_folder}")
            apply_mod(mod_path)

# Fonction pour lancer le jeu
def launch_game():
    game_exe = os.path.join(game_directory, "AstroDuel2_EOS.exe")
    subprocess.run([game_exe], check=True)

# Appliquer les mods, sauvegarder les fichiers, et lancer le jeu
if __name__ == "__main__":
    # Sauvegarder les fichiers du jeu
    backup_game_files()
    # Charger et appliquer tous les mods
    load_all_mods()
    # Lancer le jeu
    launch_game()
