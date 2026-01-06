import os
import pyperclip
from tkinter import Tk, filedialog

def generer_arborescence_compacte(dossier):
    arborescence = []
    arborescence.append(os.path.basename(dossier))  # Ajouter le nom du dossier de base
    for racine, sous_dossiers, fichiers in os.walk(dossier):
        chemin_relatif = os.path.relpath(racine, dossier)
        if chemin_relatif == ".":
            chemin_relatif = ""

        # Afficher les sous-dossiers
        for index, nom in enumerate(sous_dossiers):
            prefixe = "├ " if index < len(sous_dossiers) - 1 else "└ "
            arborescence.append(f"{chemin_relatif}/{prefixe}{nom}")
        
        # Afficher les fichiers
        for index, nom in enumerate(fichiers):
            prefixe = "├ " if index < len(fichiers) - 1 else "└ "
            arborescence.append(f"{chemin_relatif} {prefixe}{nom}")

    return "\n".join(arborescence)

# Ouvrir un explorateur de fichiers pour choisir le dossier
racine = Tk()
racine.withdraw()  # Cacher la fenêtre principale de Tkinter
chemin_du_dossier = filedialog.askdirectory(title="Choisissez un dossier")

if chemin_du_dossier:
    arborescence = generer_arborescence_compacte(chemin_du_dossier)
    pyperclip.copy(arborescence)  # Copier dans le presse-papier
    print("Structure du dossier copiée dans le presse-papier.")
else:
    print("Aucun dossier sélectionné.")
