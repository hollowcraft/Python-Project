import tkinter as tk
import pygame

pygame.init()
pygame.mixer.init()

# Notes 5e octave (ligne du haut)
notes5 = [
    ("C5", "ynstrument/notes/C5.wav"),
    ("D5", "ynstrument/notes/D5.wav"),
    ("E5", "ynstrument/notes/E5.wav"),
    ("F5", "ynstrument/notes/F5.wav"),
    ("G5", "ynstrument/notes/G5.wav"),
    ("A5", "ynstrument/notes/A5.wav"),
    ("B5", "ynstrument/notes/B5.wav"),
    ("C6", "ynstrument/notes/C6.wav"),
    ("D6", "ynstrument/notes/D6.wav"),
    ("E6", "ynstrument/notes/E6.wav"),
]

# Notes 4e octave (ligne du milieu)
notes4 = [
    ("C4", "ynstrument/notes/C4.wav"),
    ("D4", "ynstrument/notes/D4.wav"),
    ("E4", "ynstrument/notes/E4.wav"),
    ("F4", "ynstrument/notes/F4.wav"),
    ("G4", "ynstrument/notes/G4.wav"),
    ("A4", "ynstrument/notes/A4.wav"),
    ("B4", "ynstrument/notes/B4.wav"),
    ("C5", "ynstrument/notes/C5.wav"),
    ("D5", "ynstrument/notes/D5.wav"),
    ("E5", "ynstrument/notes/E5.wav"),
]

# Notes 3e octave (ligne du bas)
notes3 = [
    ("C3", "ynstrument/notes/C3.wav"),
    ("D3", "ynstrument/notes/D3.wav"),
    ("E3", "ynstrument/notes/E3.wav"),
    ("F3", "ynstrument/notes/F3.wav"),
    ("G3", "ynstrument/notes/G3.wav"),
    ("A3", "ynstrument/notes/A3.wav"),
    ("B3", "ynstrument/notes/B3.wav"),
    ("C4", "ynstrument/notes/C4.wav"),
    ("D4", "ynstrument/notes/D4.wav"),
    ("E4", "ynstrument/notes/E4.wav"),
]

key_bindings = {
    "a": "C3",
    "z": "D3",
    "e": "E3",
    "r": "F3",
    "t": "G3",
    "y": "A3",
    "u": "B3",
    "i": "C4",
    "o": "D4",
    "p": "E4",
    "q": "C4",
    "s": "D4",
    "d": "E4",
    "f": "F4",
    "g": "G4",
    "h": "A4",
    "j": "B4",
    "k": "C5",
    "l": "D5",
    "m": "E5",
    "w": "F5",
    "x": "G5",
    "c": "A5",
    "v": "B5",
    "b": "C6",
    "n": "D6",
    ",": "E6",
    ";": "F6",
    ":": "G6",
    "!": "A6",
}

# Dictionnaire des notes noires (dièses) associées aux touches + Ctrl
sharp_bindings = {
    "z": "C#3",
    "e": "D#3",
    "t": "F#3",
    "y": "G#3",
    "u": "A#3",
    "i": "C#4",
    "o": "D#4",
    "q": "C#4",
    "s": "D#4",
    "f": "F#4",
    "g": "G#4",
    "h": "A#4",
    "k": "C#5",
    "l": "D#5",
    "w": "F#5",
    "x": "G#5",
    "c": "A#5",
    "b": "C#6",
    "n": "D#6",
}

# Ajoute les fichiers dièses à note_to_file
note_to_file = {note: file for note, file in notes3 + notes4 + notes5}
note_to_file.update({
    "C#3": "ynstrument/notes/Cs3.wav",
    "D#3": "ynstrument/notes/Ds3.wav",
    "F#3": "ynstrument/notes/Fs3.wav",
    "G#3": "ynstrument/notes/Gs3.wav",
    "A#3": "ynstrument/notes/As3.wav",
    "C#4": "ynstrument/notes/Cs4.wav",
    "D#4": "ynstrument/notes/Ds4.wav",
    "F#4": "ynstrument/notes/Fs4.wav",
    "G#4": "ynstrument/notes/Gs4.wav",
    "A#4": "ynstrument/notes/As4.wav",
    "C#5": "ynstrument/notes/Cs5.wav",
    "D#5": "ynstrument/notes/Ds5.wav",
    "F#5": "ynstrument/notes/Fs5.wav",
    "G#5": "ynstrument/notes/Gs5.wav",
    "A#5": "ynstrument/notes/As5.wav",
    "C#6": "ynstrument/notes/Cs6.wav",
    "D#6": "ynstrument/notes/Ds6.wav",
})

def play_note(filename):
    try:
        sound = pygame.mixer.Sound(filename)
        sound.play()
    except Exception as e:
        print(f"Erreur lecture {filename}: {e}")

root = tk.Tk()
root.title("Mini Piano")

frame_top = tk.Frame(root)
frame_top.pack(padx=10, pady=2)
frame_mid = tk.Frame(root)
frame_mid.pack(padx=10, pady=2)
frame_bot = tk.Frame(root)
frame_bot.pack(padx=10, pady=2)

for note, file in notes5:
    btn = tk.Button(frame_top, text=note, width=6)
    btn.pack(side=tk.LEFT, padx=2)
    btn.bind("<ButtonPress-1>", lambda event, f=file: play_note(f))

for note, file in notes4:
    btn = tk.Button(frame_mid, text=note, width=6)
    btn.pack(side=tk.LEFT, padx=2)
    btn.bind("<ButtonPress-1>", lambda event, f=file: play_note(f))

for note, file in notes3:
    btn = tk.Button(frame_bot, text=note, width=6)
    btn.pack(side=tk.LEFT, padx=2)
    btn.bind("<ButtonPress-1>", lambda event, f=file: play_note(f))

def on_key(event):
    # Si Ctrl est pressé, joue la note noire
    if event.state & 0x4:  # 0x4 = Ctrl sur Windows
        note = sharp_bindings.get(event.char.lower())
    else:
        note = key_bindings.get(event.char.lower())
    if note:
        filename = note_to_file.get(note)
        if filename:
            play_note(filename)

root.bind("<Key>", on_key)

root.mainloop()