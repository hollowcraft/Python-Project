import pyautogui
import time
import torch

# Définir les données d'entrée
x = torch.tensor([0, 0, 0], dtype=torch.float)

# Définir le réseau de neurones
model = torch.nn.Sequential(
    torch.nn.Linear(3, 2),
    torch.nn.Sigmoid(),
    torch.nn.Linear(2, 1),
    torch.nn.Sigmoid()
)

# Charger les poids pré-entraînés
model.load_state_dict(torch.load('model_weights.pt'))

# Boucle principale
while True:
    # Capturer une capture d'écran de l'écran de jeu
    screen = pyautogui.screenshot()

    # Prétraiter l'image (par exemple, la convertir en noir et blanc)

    # Utiliser le réseau de neurones pour prédire la prochaine action
    y_pred = model(x)

    # Traduire la sortie en une action (par exemple, sauter ou courir à gauche ou à droite)

    # Envoyer l'action à PyAutoGUI pour qu'elle soit exécutée dans le jeu
    pyautogui.press('left')

    # Attendre un court instant pour que l'action soit exécutée
    time.sleep(0.1)
