import time
import winsound

# Boucle infinie pour répéter le bip toutes les 10 minutes
while True:
    winsound.Beep(1000, 500)
    time.sleep(600)  # 600 secondes = 10 minutes
