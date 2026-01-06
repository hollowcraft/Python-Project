import tkinter as tk
from pynput import keyboard, mouse
import pygetwindow as gw
import win32gui
import win32con
import win32api
import pygame
from threading import Thread

class InputRedirector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Input Redirector")
        self.root.geometry("400x400")

        # Variables pour les cibles de redirection
        self.keyboard_mouse_target = tk.StringVar(self.root)
        self.controller_target = tk.StringVar(self.root)

        # Interface pour afficher les applications disponibles
        tk.Label(self.root, text="Clavier + Souris vers :").pack()
        self.keyboard_mouse_menu = tk.OptionMenu(self.root, self.keyboard_mouse_target, *self.get_applications())
        self.keyboard_mouse_menu.pack()

        tk.Label(self.root, text="Manette vers :").pack()
        self.controller_menu = tk.OptionMenu(self.root, self.controller_target, *self.get_applications())
        self.controller_menu.pack()

        tk.Button(self.root, text="Démarrer", command=self.start_redirect).pack()

    def get_applications(self):
        windows = gw.getAllTitles()  # Obtenir toutes les fenêtres
        app_list = [(win, gw.getWindowsWithTitle(win)[0]._hWnd) for win in windows if win]

        # Retourne uniquement les handles et nom pour sélectionner chaque fenêtre
        for i in range(len(app_list)):
            app_list[i] = f"{app_list[i][0]} ({app_list[i][1]})"  # Format "Nom (Handle)"

        return app_list

    def start_redirect(self):
        # Démarrer les threads pour capturer les inputs
        Thread(target=self.capture_keyboard_mouse).start()
        Thread(target=self.capture_controller).start()

    def capture_keyboard_mouse(self):
        try:
            target_handle = int(self.keyboard_mouse_target.get().split("(")[-1].strip(")"))  # Récupérer le handle
        except ValueError:
            print("Erreur lors de la récupération du handle de la fenêtre pour clavier/souris.")
            return

        def on_press(key):
            try:
                key_code = ord(key.char.upper())
                win32api.PostMessage(target_handle, win32con.WM_KEYDOWN, key_code, 0)
            except AttributeError:
                pass

        def on_click(x, y, button, pressed):
            if pressed:
                win32api.PostMessage(target_handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
            else:
                win32api.PostMessage(target_handle, win32con.WM_LBUTTONUP, 0, 0)

        keyboard_listener = keyboard.Listener(on_press=on_press)
        mouse_listener = mouse.Listener(on_click=on_click)

        keyboard_listener.start()
        mouse_listener.start()

    def capture_controller(self):
        pygame.init()
        pygame.joystick.init()

        try:
            target_handle = int(self.controller_target.get().split("(")[-1].strip(")"))
        except ValueError:
            print("Erreur lors de la récupération du handle de la fenêtre pour la manette.")
            return

        if pygame.joystick.get_count() > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            print("Manette détectée.")

        while True:
            pygame.event.pump()
            if joystick.get_button(0):  # Exemple : bouton A
                win32api.PostMessage(target_handle, win32con.WM_KEYDOWN, ord('A'), 0)
            elif joystick.get_button(1):  # Exemple : bouton B
                win32api.PostMessage(target_handle, win32con.WM_KEYDOWN, ord('B'), 0)
            # Rediriger d'autres boutons ou axes de la manette selon besoin

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = InputRedirector()
    app.run()
