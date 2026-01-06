import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

def select_file():
    file_path = filedialog.askopenfilename(
        title="Choisir un raccourci .url",
        filetypes=[("Raccourci Internet", "*.url")]
    )
    if not file_path:
        return
    
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Récupérer l'URL du fichier .url
    url_line = [line for line in content.splitlines() if line.startswith("URL=")]
    if not url_line:
        messagebox.showerror("Erreur", "Impossible de trouver l'URL dans ce raccourci.")
        return

    url = url_line[0].replace("URL=", "").strip()

    # Créer un script temporaire qui ouvre l'URL
    script_code = f'''import subprocess
subprocess.run(["cmd", "/c", "start", "", "{url}"], shell=True)
'''
    temp_script = "launcher_temp.py"
    with open(temp_script, "w", encoding="utf-8") as f:
        f.write(script_code)

    # Compiler en .exe avec PyInstaller
    try:
        subprocess.run([
            "pyinstaller",
            "--onefile",
            "--noconsole",
            "--distpath", ".",
            temp_script
        ], check=True)
        messagebox.showinfo("Succès", "L'exécutable a été créé avec succès !")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de compiler : {e}")
    finally:
        # Nettoyer les fichiers temporaires
        for item in ["build", "__pycache__", temp_script, temp_script.replace(".py", ".spec")]:
            if os.path.isdir(item):
                subprocess.run(["rmdir", "/s", "/q", item], shell=True)
            elif os.path.isfile(item):
                os.remove(item)

# Interface Tkinter
root = tk.Tk()
root.title("Convertir .url en .exe")
root.geometry("300x150")

btn_select = tk.Button(root, text="Choisir un raccourci .url", command=select_file)
btn_select.pack(pady=40)

root.mainloop()
