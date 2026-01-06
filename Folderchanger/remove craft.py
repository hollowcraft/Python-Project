import os
import json
import shutil
import tkinter as tk
from tkinter import filedialog

def replace_json_content():
    # Créer la fenêtre de sélection de dossier
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale de Tkinter
    folder_path = filedialog.askdirectory(title="Choisissez un dossier")

    if not folder_path:
        print("Aucun dossier sélectionné. Fin du programme.")
        return

    # Définir les chemins du script et du fichier Craft.json
    script_dir = os.path.dirname(os.path.abspath(__file__))
    craft_path = os.path.join(script_dir, "text.txt")

    # Charger le contenu de Craft.json
    try:
        with open(craft_path, 'r', encoding='utf-8') as craft_file:
            craft_content = json.load(craft_file)
    except FileNotFoundError:
        print(f"Le fichier 'Craft.json' est introuvable dans {script_dir}.")
        return

    # Créer une copie temporaire du dossier sélectionné dans le dossier du script
    temp_folder_path = os.path.join(script_dir, os.path.basename(folder_path) + "_temp")
    try:
        shutil.copytree(folder_path, temp_folder_path)
        print(f"Dossier temporaire créé avec succès : {temp_folder_path}")
    except FileExistsError:
        print(f"Le dossier temporaire '{temp_folder_path}' existe déjà. Veuillez le supprimer ou renommer.")
        return

    # Remplacer le contenu de chaque fichier .json dans le dossier temporaire
    for root_dir, _, files in os.walk(temp_folder_path):
        for file_name in files:
            if file_name.endswith('.tmx'):
                file_path = os.path.join(root_dir, file_name)
                try:
                    with open(file_path, 'w', encoding='utf-8') as json_file:
                        json.dump(craft_content, json_file, indent=4, ensure_ascii=False)
                    print(f"Contenu de {file_name} remplacé avec succès.")
                except Exception as e:
                    print(f"Erreur lors de la modification de {file_name} : {e}")

    # Supprimer le dossier original et déplacer le dossier temporaire pour le remplacer
    try:
        shutil.rmtree(folder_path)
        shutil.move(temp_folder_path, folder_path)
        print(f"Dossier original remplacé avec succès par la version modifiée.")
    except Exception as e:
        print(f"Erreur lors du remplacement du dossier : {e}")

if __name__ == "__main__":
    replace_json_content()
