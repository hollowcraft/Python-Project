import pyautogui
import time

# Attendre 5 secondes avant de commencer
time.sleep(5)
print("start")

# Appuyez sur la touche "espace" pour sauter pendant 1 seconde 
pyautogui.keyDown('space')
time.sleep(1)
pyautogui.keyUp('space')

# Appuyez sur la touche "gauche" pendant 1 seconde pour se deplacer vers la gauche
pyautogui.keyDown('q')
time.sleep(1)
pyautogui.keyUp('q')

# Appuyez sur la touche "droite" pendant 1 seconde pour se deplacer vers la droite
pyautogui.keyDown('d')
time.sleep(1)
pyautogui.keyUp('d')

# Relacher la touche "espace" pour arreter de sauter


 
