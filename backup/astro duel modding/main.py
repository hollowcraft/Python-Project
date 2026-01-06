import tkinter as tk
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET

class LevelEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("XML Level Editor")

        # Bouton pour charger le fichier
        self.load_button = tk.Button(root, text="Charger Niveau XML", command=self.load_level)
        self.load_button.pack()

        # Cadre pour afficher les informations de propriété
        self.info_frame = tk.Frame(root)
        self.info_frame.pack()

        # Texte pour les propriétés
        self.properties_text = tk.Text(self.info_frame, width=50, height=10)
        self.properties_text.pack()

        # Cadre pour afficher la matrice de chaque couche
        self.matrix_frame = tk.Frame(root)
        self.matrix_frame.pack()

        # Dictionnaire pour stocker les couches
        self.layers = []

    def load_level(self):
        # Charger un fichier XML
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers XML", "*.xml *.tmx")])
        if not file_path:
            return

        try:
            self.tree = ET.parse(file_path)
            self.root_elem = self.tree.getroot()
            self.display_properties()
            self.load_layers()
            self.display_all_layers()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le fichier XML:\n{e}")

    def display_properties(self):
        # Effacer le texte précédent
        self.properties_text.delete(1.0, tk.END)
        
        # Afficher les propriétés du niveau
        properties = self.root_elem.find("properties")
        if properties:
            for prop in properties:
                name = prop.attrib.get("name")
                value = prop.attrib.get("value")
                self.properties_text.insert(tk.END, f"{name}: {value}\n")
        else:
            self.properties_text.insert(tk.END, "Aucune propriété trouvée.")

    def load_layers(self):
        # Charger toutes les couches du fichier XML
        self.layers = self.root_elem.findall("layer")

    def display_all_layers(self):
        # Effacer le cadre précédent
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        # Parcourir et afficher chaque couche
        for layer in self.layers:
            self.display_layer(layer)

    def display_layer(self, layer):
        # Charger la matrice de la couche
        layer_name = layer.attrib.get("name", "Layer")
        width = int(layer.attrib.get("width", 0))
        height = int(layer.attrib.get("height", 0))
        data_elem = layer.find("data")

        if data_elem is not None and data_elem.text:
            tile_data = list(map(int, data_elem.text.strip().split(',')))
            matrix = [tile_data[i * width:(i + 1) * width] for i in range(height)]

            # Titre de la couche
            tk.Label(self.matrix_frame, text=f"--- {layer_name} ---").pack()

            # Afficher la matrice sous forme de couleurs
            for i, row in enumerate(matrix):
                row_frame = tk.Frame(self.matrix_frame)
                row_frame.pack()
                for j, tile in enumerate(row):
                    color = self.get_tile_color(tile)
                    label = tk.Label(row_frame, bg=color, width=2, height=1)
                    label.pack(side=tk.LEFT)

    def get_tile_color(self, tile_value):
        # Exemple de couleurs personnalisées par valeur
        color_mapping = {
            0: "#ff0000",   # Rouge
            1: "#00ff00",   # Vert
            2: "#0000ff",   # Bleu
            3: "#ffff00",   # Jaune
            4: "#ff00ff",   # Magenta
            5: "#00ffff",   # Cyan
            77: "#000000",  # Noir
            # Ajoutez d'autres mappings selon les besoins
        }

        return color_mapping.get(tile_value, "#ffffff")  # Blanc par défaut pour les valeurs inconnues

    def save_level(self):
        # Enregistrer les modifications dans le fichier XML
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".tmx", filetypes=[("Fichiers TMX", "*.tmx")])
            if not file_path:
                return
            self.tree.write(file_path)
            messagebox.showinfo("Succès", "Fichier XML sauvegardé avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde du fichier XML:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LevelEditor(root)
    root.mainloop()
