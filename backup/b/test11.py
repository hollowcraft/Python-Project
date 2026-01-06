import pyautogui
import time
from PIL import Image

# Attendre 5 secondes avant de commencer
time.sleep(5)
print("start")

# premier saut
pyautogui.press('F8')

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
time.sleep(0.35)
pyautogui.keyDown('shift')
pyautogui.keyUp('d')
pyautogui.keyUp('space')
pyautogui.keyUp('z')
pyautogui.keyDown('z')
time.sleep(0.15)
pyautogui.keyUp('shift')

pyautogui.keyDown('space')
pyautogui.keyDown('z')
time.sleep(0.25)
pyautogui.keyDown('shift')
time.sleep(0.25)
pyautogui.keyUp('shift')
pyautogui.keyUp('space')
pyautogui.keyUp('z')




 
