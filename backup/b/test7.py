import pyautogui
import time
from PIL import Image

# Attendre 5 secondes avant de commencer
time.sleep(5)
print("start")

# premier saut
# pyautogui.press('F7')

pyautogui.keyDown('d')
time.sleep(0.25)
pyautogui.keyDown('space')
time.sleep(0.25)
pyautogui.keyUp('d')
pyautogui.keyUp('space')

pyautogui.keyDown('d')
pyautogui.keyDown('space')
pyautogui.keyDown('z')
time.sleep(1)
pyautogui.keyUp('d')
pyautogui.keyUp('space')
pyautogui.keyUp('z')

pyautogui.keyDown('d')
pyautogui.keyDown('space')
pyautogui.keyDown('z')
time.sleep(0.5)
pyautogui.press('x')
pyautogui.keyUp('d')
pyautogui.keyUp('space')
pyautogui.keyUp('z')

pyautogui.keyDown('space')
pyautogui.keyDown('z')
time.sleep(0.25)
pyautogui.press('x')
time.sleep(0.5)
pyautogui.press('x')
pyautogui.keyUp('space')
pyautogui.keyUp('z')


time.sleep(5)
# pyautogui.press('F8')


# Appuyez sur la touche "espace" pour sauter pendant 1 seconde 
pyautogui.keyDown('space')
time.sleep(1)
pyautogui.keyUp('space')

# Appuyez sur la touche "q" pendant 1 seconde
pyautogui.keyDown('q')
time.sleep(1)
pyautogui.keyUp('q')

# Appuyez sur la touche "d" pendant 1 seconde
pyautogui.keyDown('d')
time.sleep(1)
pyautogui.keyUp('d')

# Appuyez sur la touche "z" pendant 1 seconde
pyautogui.keyDown('z')
time.sleep(1)
pyautogui.keyUp('z')


 
