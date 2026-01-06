import pyttsx3
import tkinter as tk
from tkinter import simpledialog

def lire_texte():
    texte = champ_texte.get()
    repetitions = 5  # Modifier si besoin
    pause = 2  # Pause entre chaque répétition en secondes
    
    if texte.strip():  # Vérifie si le texte n'est pas vide
        engine = pytt
