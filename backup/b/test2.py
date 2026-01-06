import pyautogui
import time

# Attendre 5 secondes avant de commencer
time.sleep(5)

# Appuyez sur la touche "espace" pour sauter
pyautogui.keyDown('space')

# Appuyez sur la touche "gauche" pendant 1 seconde pour se deplacer vers la gauche
pyautogui.keyDown('left')
time.sleep(1)
pyautogui.keyUp('left')

# Appuyez sur la touche "droite" pendant 1 seconde pour se deplacer vers la droite
pyautogui.keyDown('right')
time.sleep(1)
pyautogui.keyUp('right')

# Relacher la touche "espace" pour arreter de sauter
pyautogui.keyUp('space')
