import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import winsound
import time
import keyboard

def load_ban_words(filename="C:/Users/Adam/Desktop/Mes Projects/python/voice/banWord.txt"):
    """Charge les mots interdits depuis un fichier texte"""
    with open(filename, "r", encoding="utf-8") as file:
        ban_words = {line.strip().lower() for line in file}
    return ban_words

def play_beep():
    """Joue un bip sonore avec winsound"""
    frequency = 1000  # Fréquence du bip en Hertz
    duration = 300  # Durée du bip en millisecondes
    winsound.Beep(frequency, duration)

def capture_and_amplify_voice():
    recognizer = sr.Recognizer()
    calibration_count = 0
    ban_words = load_ban_words()  # Charge les mots bannis
    
    while True:
        if keyboard.is_pressed('alt'):  # Vérifie si la touche TAB est pressée
            with sr.Microphone() as source:
                if calibration_count % 10 == 0:
                    print("Calibrage du bruit ambiant...")
                    recognizer.adjust_for_ambient_noise(source)
                    load_ban_words()
                    time.sleep(1)

                print("Parlez maintenant... (ou dites 'arrêter' pour quitter)")

                try:
                    audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    print("Enregistrement terminé, traitement en cours...")

                    # Convertir en texte
                    text = recognizer.recognize_google(audio_data, language="fr-FR")
                    print("Vous avez dit :", text)

                    # Si l'utilisateur dit "arrêter", on quitte la boucle
                    if text.lower() == "arrêter":
                        print("Arrêt de la reconnaissance vocale.")
                        break
                    
                    # Vérifier les mots bannis
                    if any(ban_word in text.lower() for ban_word in ban_words):
                        print("Mot interdit détecté!")
                        play_beep()

                    # Ajuster le volume de l'enregistrement
                    audio_segment = AudioSegment(data=audio_data.get_wav_data(), sample_width=2, frame_rate=16000, channels=1)
                    louder_audio = audio_segment + 20

                    calibration_count += 1

                except sr.UnknownValueError:
                    print("Je n'ai pas compris ce que vous avez dit.")
                except sr.RequestError as e:
                    print("Erreur de reconnaissance vocale ; vérifiez votre connexion Internet :", e)
                except Exception as e:
                    print("Une erreur est survenue :", e)

capture_and_amplify_voice()
