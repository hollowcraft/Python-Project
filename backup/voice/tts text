import pyttsx3

path = "C:/Users/Adam/Desktop/Mes Projects/python/voice/text.txt"

# Définir le volume (entre 0.0 et 1.0)
volume = 0.6

# Ouvre et lit le contenu du fichier text.txt
with open(path, 'r', encoding='utf-8') as f:
    texte = f.read()

while 1==1:
    engine = pyttsx3.init()
    engine.setProperty('volume', volume)
    engine.say(texte)
    engine.runAndWait()