import tkinter as tk
import numpy as np
import sounddevice as sd
import threading

root = tk.Tk()
root.title(0)
root.geometry("270x289")

notes = {
    "0": 0,
    "C": 262,
    "C#": 277,
    "D": 294,
    "D#": 311,
    "E": 330,
    "F": 349,
    "F#": 370,
    "G": 392,
    "G#": 415,
    "A": 440,
    "A#": 466,
    "B": 494,
    "2C": 523,
    "2C#": 554,
    "2D": 587,
    "2D#": 622,
    "2E": 659,
    "2F": 698,
    "2F#": 740,
    "2G": 784,
    "2G#": 831,
    "2A": 880,
    "2A#": 932,
    "2B": 988
}

bNotes = {
    1: "F#", 2: "2C#", 3: "2G#",
    4: "G#", 5: "A#", 6: "2F#",
    7: "B", 8: "2D#", 9: "2E"
},{
    1: "B", 2: "C#", 3: "D#",
    4: "E", 5: "F#", 6: "G#",
    7: "2B", 8: "0", 9: "0"
}

config = 0

def Num2Note(note_name):
    if note_name in notes:
        return note_name
    else:
        return None

sample_rate = 44100
duration = 10

playing_flags = {}

fade_time = 0.1  # durée du fade en secondes

def generate_tone(frequency, duration=duration, sample_rate=sample_rate):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    tone = 0.3 * np.sin(2 * np.pi * frequency * t)
    return tone.astype(np.float32)

def apply_fade(tone, sample_rate, fade_time):
    fade_samples = int(sample_rate * fade_time)
    envelope = np.ones_like(tone)

    # fade in
    fade_in_curve = np.linspace(0, 1, fade_samples)
    envelope[:fade_samples] = fade_in_curve

    # fade out
    fade_out_curve = np.linspace(1, 0, fade_samples)
    envelope[-fade_samples:] = fade_out_curve

    return tone * envelope

def play_note_loop(frequency, flag):
    tone = generate_tone(frequency)
    tone = apply_fade(tone, sample_rate, fade_time)
    stream = sd.OutputStream(samplerate=sample_rate, channels=1)
    stream.start()
    idx = 0
    buffer_size = 1024

    # Pour fade out progressif lors de l'arrêt
    fade_out_samples = int(sample_rate * fade_time)
    fade_out_step = 1 / (fade_out_samples / buffer_size)  # combien réduire par buffer

    current_volume = 1.0

    while flag['playing']:
        if idx + buffer_size > len(tone):
            idx = 0  # boucle normale
        data = tone[idx:idx+buffer_size]
        stream.write(data)
        idx += buffer_size

    # fade out progressif avant d’arrêter
    while current_volume > 0:
        chunk = tone[idx:idx+buffer_size] if idx + buffer_size <= len(tone) else tone[0:buffer_size - (len(tone)-idx)]
        chunk = chunk * current_volume
        stream.write(chunk)
        current_volume -= fade_out_step
        if idx + buffer_size > len(tone):
            idx = 0
        else:
            idx += buffer_size

    stream.stop()
    stream.close()

def start_playing(key):
    note_name = bNotes[config].get(key, None)
    if note_name is None:
        return
    note = Num2Note(note_name)
    if note is None:
        return
    if key in playing_flags and playing_flags[key]['playing']:
        return
    flag = {'playing': True}
    playing_flags[key] = flag
    t = threading.Thread(target=play_note_loop, args=(notes[note], flag), daemon=True)
    t.start()
    print(f"{key}")

def stop_playing(key):
    if key in playing_flags:
        playing_flags[key]['playing'] = False
        print(f"{key} X")

for ligne in range(3):
    for colonne in range(3):
        num = ligne * 3 + colonne + 1
        bouton = tk.Button(root, text=str(num), width=10, height=5)
        bouton.grid(row=ligne, column=colonne, padx=5, pady=5)
        bouton.bind('<ButtonPress-1>', lambda e, n=num: start_playing(n))
        bouton.bind('<ButtonRelease-1>', lambda e, n=num: stop_playing(n))

for key in range(1, 10):
    root.bind(f"<KeyPress-{key}>", lambda e, k=key: start_playing(k+(int((k-1)/3)-1)*-6))
    root.bind(f"<KeyRelease-{key}>", lambda e, k=key: stop_playing(k+(int((k-1)/3)-1)*-6))
    

def update_config(value):
    global config
    if config + value < 0:
        config = len(bNotes) - 1
    elif config + value >= len(bNotes):
        config = 0
    else:
        config += value
    print("Config =", config)
    root.title(config)

root.bind("<Left>",  lambda e: update_config(-1))
root.bind("<Right>", lambda e: update_config(1))

root.mainloop()
