import tkinter as tk
from tkinter import messagebox
import keyboard
import pygetwindow as gw
import winsound
import threading

class PianoApp:
    def __init__(self):
        self.piano_window = None
        self.previous_window = None
        self.is_piano_active = False

        # Notes du piano (clavier -> fréquence)
        self.notes = {
            'a': 261.63,  # Do
            'z': 293.66,  # Ré
            'e': 329.63,  # Mi
            'r': 349.23,  # Fa
            't': 392.00,  # Sol
            'y': 440.00,  # La
            'u': 493.88,  # Si
            'i': 523.25   # Do (octave supérieure)
        }

        # Lancer le gestionnaire de raccourcis dans un thread séparé
        threading.Thread(target=self.listen_shortcut, daemon=True).start()

    def listen_shortcut(self):
        """Écoute le raccourci clavier pour activer/désactiver le piano."""
        while True:
            # Raccourci pour activer/désactiver le piano (Ctrl+P)
            keyboard.wait("ctrl+p")
            if self.is_piano_active:
                self.close_piano()
            else:
                self.open_piano()

    def open_piano(self):
        """Ouvre le piano virtuel."""
        # Sauvegarder la fenêtre active
        self.previous_window = gw.getActiveWindow()
        print(f"Previous window: {self.previous_window}")

        # Créer la fenêtre du piano
        self.piano_window = tk.Tk()
        self.piano_window.title("Virtual Piano")
        self.piano_window.geometry("600x200")
        self.piano_window.protocol("WM_DELETE_WINDOW", self.close_piano)

        # Ajouter des touches pour chaque note
        for key, freq in self.notes.items():
            btn = tk.Button(self.piano_window, text=key.upper(), width=5, height=2,
                            command=lambda f=freq: self.play_note(f))
            btn.pack(side=tk.LEFT, padx=5, pady=20)

        self.is_piano_active = True
        self.piano_window.mainloop()

    def close_piano(self):
        """Ferme le piano virtuel et revient à l'application précédente."""
        if self.piano_window:
            self.piano_window.destroy()
            self.piano_window = None
            self.is_piano_active = False

        # Restaurer la fenêtre précédente
        if self.previous_window:
            self.previous_window.activate()

    def play_note(self, frequency):
        """Joue une note avec la fréquence donnée."""
        duration = 300  # Durée de la note en millisecondes
        winsound.Beep(int(frequency), duration)


if __name__ == "__main__":
    try:
        app = PianoApp()
        messagebox.showinfo("Piano Shortcut", "Appuyez sur Ctrl+P pour activer/désactiver le piano.")
    except Exception as e:
        print(f"Erreur : {e}")