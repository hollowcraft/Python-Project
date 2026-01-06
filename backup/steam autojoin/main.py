import pyautogui
import time

time.sleep(1)
# Récupère la position actuelle de la souris
x, y = pyautogui.position()

# Capture l'écran à la position de la souris
pixel_color = pyautogui.screenshot().getpixel((x, y))

print(pixel_color)
while 1==1:
    if pixel_color == (208, 217, 233):  # Couleur rouge
        pyautogui.click()
        break