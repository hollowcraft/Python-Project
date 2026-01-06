import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import random
import shutil

SAVE_DIR = r"C:\\Users\\Adam\\AppData\\LocalLow\\Hopoo Games, LLC\\Risk of Rain 2\\ProperSave\\Saves"
ITEMS_JSON = "ItemName.json"
BACKUP_DIR = os.path.join(SAVE_DIR, "backup")

class StyleConfig:
    """Configuration des styles de l'application"""
    # Couleurs
    BG_DARK = "#2C2F33"
    BG_MEDIUM = "#23272A"
    BG_LIGHT = "#295A75"
    TEXT_COLOR = "#FFFFFF"
    ACCENT_COLOR = "#7289DA"
    BUTTON_BG = "#7289DA"
    BUTTON_FG = "#FFFFFF"
    BUTTON_ACTIVE_BG = "#677BC4"
    
    # Couleurs des raretés
    RARITY_COLORS = {
        0: "#808080",  # Gris pour unknown
        1: "#9B9B9B",  # Gris clair pour commun
        2: "#1AC73D",  # Vert
        3: "#C71A1A",  # Rouge
        4: "#E8BE0C",  # Jaune
        5: "#8B1AC7",  # Violet pour void
        6: "#00B4E6"   # Bleu clair pour lunar
    }
    
    # Noms des raretés
    RARITY_NAMES = {
        0: "Inconnu",
        1: "Commun",
        2: "Peu commun",
        3: "Légendaire",
        4: "Boss",
        5: "Void",
        6: "Lunar"
    }
    
    # Polices
    FONT_MAIN = ("Helvetica", 10)
    FONT_TITLE = ("Helvetica", 12, "bold")
    FONT_BUTTON = ("Helvetica", 9)
    
    @classmethod
    def apply_style(cls, root):
        """Applique le style à l'application"""
        style = ttk.Style()
        style.theme_use('clam')  # Utilise le thème 'clam' qui est plus moderne
        
        # Configuration des onglets
        style.configure("TNotebook", background=cls.BG_DARK)
        style.configure("TNotebook.Tab", background=cls.BG_MEDIUM, foreground=cls.TEXT_COLOR, padding=[10, 2])
        style.map("TNotebook.Tab",
                 background=[("selected", cls.ACCENT_COLOR)],
                 foreground=[("selected", cls.TEXT_COLOR)])
        
        # Configuration des frames
        style.configure("TFrame", background=cls.BG_DARK)
        
        # Configuration générale
        root.configure(bg=cls.BG_DARK)

class ROR2SaveEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Risk of Rain 2 - Save Editor")
        
        # Variables pour le copier/coller
        self.clipboard_items = None
        
        # Appliquer le style
        StyleConfig.apply_style(self.root)
        
        # Création du dossier backup s'il n'existe pas
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)
        
        # Frame gauche pour la liste des sauvegardes
        self.frame_left = tk.Frame(self.root, width=200, bg=StyleConfig.BG_MEDIUM)
        self.frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Titre de la liste des sauvegardes
        title_label = tk.Label(self.frame_left, 
                             text="Sauvegardes", 
                             font=StyleConfig.FONT_TITLE,
                             bg=StyleConfig.BG_MEDIUM,
                             fg=StyleConfig.TEXT_COLOR)
        title_label.pack(pady=(5,10))
        
        # Liste des sauvegardes avec scrollbar
        listbox_frame = tk.Frame(self.frame_left, bg=StyleConfig.BG_MEDIUM)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox_saves = tk.Listbox(listbox_frame,
                                      bg=StyleConfig.BG_LIGHT,
                                      fg=StyleConfig.TEXT_COLOR,
                                      font=StyleConfig.FONT_MAIN,
                                      selectmode=tk.SINGLE,
                                      yscrollcommand=scrollbar.set)
        self.listbox_saves.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox_saves.yview)
        
        self.listbox_saves.bind("<Double-1>", self.load_save)
        
        # Bouton de mise à jour
        self.btn_update = tk.Button(self.frame_left,
                                  text="Mettre à jour",
                                  command=self.update_file,
                                  bg=StyleConfig.BUTTON_BG,
                                  fg=StyleConfig.BUTTON_FG,
                                  font=StyleConfig.FONT_BUTTON,
                                  activebackground=StyleConfig.BUTTON_ACTIVE_BG,
                                  relief=tk.FLAT,
                                  cursor="hand2")
        self.btn_update.pack(fill=tk.X, pady=(5,0))
        
        # Notebook pour les onglets
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.saves = []
        self.items_data = {}
        self.current_save_index = None
        self.entries = {}
        self.character_entries = {}
        self.arsenal_entries = {}
        
        self.load_items_data()
        self.load_saves()
        
        # Menu contextuel
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Open", command=self.load_save)
        self.context_menu.add_command(label="Refresh", command=self.refresh_save)
        self.context_menu.add_command(label="Randomize", command=self.randomize_items)
        self.context_menu.add_command(label="Restore Backup", command=self.restore_backup)

        # Clic droit sur la liste des sauvegardes
        self.listbox_saves.bind("<Button-3>", self.show_context_menu)
        
    def show_context_menu(self, event):
        """Affiche le menu contextuel à l'endroit du clic droit"""
        selected = self.listbox_saves.nearest(event.y)
        if selected != -1:
            self.current_save_index = selected
            self.context_menu.post(event.x_root, event.y_root)
        
    def load_items_data(self):
        """Charge le JSON des items."""
        # Obtenir le chemin absolu du fichier JSON
        json_path = os.path.join(os.path.dirname(__file__), ITEMS_JSON)
        
        try:
            if not os.path.exists(json_path):
                messagebox.showerror("Erreur", f"Le fichier {ITEMS_JSON} n'existe pas dans le dossier du programme.")
                self.items_data = {}
                return
                
            with open(json_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    # Organiser les items par rareté
                    self.items_data = {}
                    for item_id, item_info in data.items():
                        if isinstance(item_info, dict):
                            name = item_info.get("name", f"ID: {item_id}")
                            rarity = item_info.get("rarity", 0)
                        else:
                            name = str(item_info)
                            rarity = 0
                        self.items_data[item_id] = {"name": name, "rarity": rarity}
                        
                except json.JSONDecodeError as e:
                    messagebox.showerror("Erreur", f"Le fichier {ITEMS_JSON} n'est pas un JSON valide.\nErreur: {str(e)}")
                    self.items_data = {}
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la lecture du fichier {ITEMS_JSON}.\nErreur: {str(e)}")
            self.items_data = {}
        
    def get_sorted_items(self, items):
        """Trie les items par rareté et par nom."""
        sorted_items = []
        for item in items:
            if isinstance(item, dict) and "i" in item and "c" in item:
                item_id = str(item["i"])
                item_data = self.items_data.get(item_id, {"name": f"ID: {item_id}", "rarity": 0})
                sorted_items.append({
                    "id": item_id,
                    "count": item["c"],
                    "name": item_data["name"],
                    "rarity": item_data["rarity"]
                })
        
        return sorted(sorted_items, key=lambda x: (x["rarity"], x["name"]))

    def create_rarity_header(self, grid_frame, current_rarity, row):
        """Crée un en-tête pour une nouvelle section de rareté."""
        # Ajouter un espace avant le nouvel en-tête (sauf pour le premier)
        if row > 1:
            row += 1
            
        # Créer l'en-tête de rareté
        rarity_name = StyleConfig.RARITY_NAMES.get(current_rarity, "Inconnu")
        header = tk.Label(grid_frame,
                         text=f"▼ {rarity_name}",
                         bg=StyleConfig.BG_DARK,
                         fg=StyleConfig.RARITY_COLORS.get(current_rarity, StyleConfig.TEXT_COLOR),
                         font=StyleConfig.FONT_TITLE)
        header.grid(row=row, column=0, columnspan=2, sticky="w", pady=(10, 5), padx=5)
        row += 1
        return row

    def display_items(self, grid_frame, sorted_items):
        """Affiche les items triés avec des en-têtes de rareté."""
        row = 0
        current_rarity = None
        
        # En-têtes des colonnes
        tk.Label(grid_frame,
                text="Item",
                bg=StyleConfig.BG_DARK,
                fg=StyleConfig.TEXT_COLOR,
                font=StyleConfig.FONT_TITLE).grid(row=row, column=0, sticky="w", pady=(0,10), padx=5)
        tk.Label(grid_frame,
                text="Quantité",
                bg=StyleConfig.BG_DARK,
                fg=StyleConfig.TEXT_COLOR,
                font=StyleConfig.FONT_TITLE).grid(row=row, column=1, sticky="w", pady=(0,10), padx=5)
        row += 1
        
        for item in sorted_items:
            if item["rarity"] != current_rarity:
                current_rarity = item["rarity"]
                row = self.create_rarity_header(grid_frame, current_rarity, row)
            
            # Label pour le nom de l'item
            item_name = item["name"].strip('"').strip("'")  # Nettoyer le nom une deuxième fois par sécurité
            label = tk.Label(grid_frame,
                           text=item_name,
                           bg=StyleConfig.BG_DARK,
                           fg=StyleConfig.RARITY_COLORS.get(current_rarity, StyleConfig.TEXT_COLOR),
                           font=StyleConfig.FONT_MAIN,
                           anchor="w",
                           justify="left")
            label.grid(row=row, column=0, sticky="w", padx=5, pady=2)
            
            # Entry pour la quantité
            entry = tk.Entry(grid_frame,
                           width=10,
                           bg=StyleConfig.BG_MEDIUM,
                           fg=StyleConfig.TEXT_COLOR,
                           font=StyleConfig.FONT_MAIN,
                           justify="center")
            entry.insert(0, str(item["count"]))
            entry.grid(row=row, column=1, sticky="w", padx=5, pady=2)
            
            # Stocker l'entry pour la mise à jour
            self.item_entries[item["id"]] = entry
            row += 1
            
        return row

    def load_saves(self):
        """Charge automatiquement les fichiers de sauvegarde."""
        if not os.path.exists(SAVE_DIR):
            return
        
        for filename in os.listdir(SAVE_DIR):
            if filename.endswith(".json"):
                filepath = os.path.join(SAVE_DIR, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.saves.append((filepath, data))
                    self.listbox_saves.insert(tk.END, filename)

    def load_save(self, event=None):
        """Charge une sauvegarde et affiche les informations générales et les joueurs."""
        selected = self.listbox_saves.curselection()
        if not selected:
            return
        
        self.current_save_index = selected[0]
        filepath, save_data = self.saves[selected[0]]
        
        for widget in self.notebook.winfo_children():
            widget.destroy()
        
        self.entries = {}
        self.character_entries = {}
        self.item_entries = {}
        
        players = save_data.get("p", [])
        for player_index, player in enumerate(players):
            player_name = f"Joueur {player_index + 1}"
            if "si" in player and "s" in player["si"]:
                player_name = f"Joueur {player['si']['s']}"
            
            player_tab = ttk.Frame(self.notebook)
            self.notebook.add(player_tab, text=player_name)
            
            # Frame pour les informations du personnage
            char_frame = tk.Frame(player_tab, bg=StyleConfig.BG_MEDIUM, pady=10, padx=5)
            char_frame.pack(fill=tk.X)
            
            tk.Label(char_frame,
                    text="Personnage:",
                    bg=StyleConfig.BG_MEDIUM,
                    fg=StyleConfig.TEXT_COLOR,
                    font=StyleConfig.FONT_MAIN).pack(side=tk.LEFT)
                    
            char_entry = tk.Entry(char_frame,
                                bg=StyleConfig.BG_LIGHT,
                                fg=StyleConfig.TEXT_COLOR,
                                font=StyleConfig.FONT_MAIN)
            char_entry.insert(0, player.get("m", {}).get("bn", "Unknown"))
            char_entry.pack(side=tk.LEFT, padx=5)
            self.character_entries[player['si']['s']] = char_entry
            
            # Frame pour l'arsenal du joueur
            arsenal_frame = tk.Frame(player_tab, bg=StyleConfig.BG_MEDIUM, pady=10, padx=5)
            arsenal_frame.pack(fill=tk.X)
            
            tk.Label(arsenal_frame,
                    text="Arsenal:",
                    bg=StyleConfig.BG_MEDIUM,
                    fg=StyleConfig.TEXT_COLOR,
                    font=StyleConfig.FONT_TITLE).pack(side=tk.LEFT, padx=(0, 10))
            
            # Récupérer l'arsenal du joueur
            arsenal = player.get("m", {}).get("l", {}).get("ml", [])
            
            # Créer un frame pour chaque slot d'équipement
            for slot_index, slot in enumerate(arsenal):
                slot_frame = tk.Frame(arsenal_frame, bg=StyleConfig.BG_MEDIUM)
                slot_frame.pack(side=tk.LEFT, padx=5)
                
                # Label pour le numéro du slot
                tk.Label(slot_frame,
                        text=f"Slot {slot_index + 1}:",
                        bg=StyleConfig.BG_MEDIUM,
                        fg=StyleConfig.TEXT_COLOR,
                        font=StyleConfig.FONT_MAIN).pack(side=tk.LEFT)
                
                # Entry pour l'ID de l'équipement
                entry = tk.Entry(slot_frame,
                               width=8,
                               bg=StyleConfig.BG_LIGHT,
                               fg=StyleConfig.TEXT_COLOR,
                               font=StyleConfig.FONT_MAIN)
                entry.insert(0, str(slot.get("bi", "")))
                entry.pack(side=tk.LEFT, padx=2)
                
                # Stocker l'entrée dans le dictionnaire
                if player['si']['s'] not in self.arsenal_entries:
                    self.arsenal_entries[player['si']['s']] = []
                self.arsenal_entries[player['si']['s']].append((slot_index, entry))
            
            # Frame pour les items avec scrollbar
            items_container = tk.Frame(player_tab, bg=StyleConfig.BG_DARK)
            items_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            canvas = tk.Canvas(items_container, bg=StyleConfig.BG_DARK)
            scrollbar = tk.Scrollbar(items_container, orient="vertical", command=canvas.yview)
            items_frame = tk.Frame(canvas, bg=StyleConfig.BG_DARK)
            
            canvas.configure(yscrollcommand=scrollbar.set)
            
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            canvas.create_window((0, 0), window=items_frame, anchor="nw")
            
            # Créer un frame pour la grille des items
            grid_frame = tk.Frame(items_frame, bg=StyleConfig.BG_DARK)
            grid_frame.pack(fill=tk.BOTH, expand=True, padx=10)
            
            # Menu contextuel pour les items
            items_context_menu = tk.Menu(grid_frame, tearoff=0)
            items_context_menu.add_command(label="Copier les items", command=lambda p=player: self.copy_items(p))
            items_context_menu.add_command(label="Coller les items", command=lambda p=player: self.paste_items(p))
            
            # Bind le menu contextuel et les raccourcis
            grid_frame.bind("<Button-3>", lambda e, m=items_context_menu: self.show_items_menu(e, m))
            grid_frame.bind("<Control-c>", lambda e, p=player: self.copy_items(p))
            grid_frame.bind("<Control-v>", lambda e, p=player: self.paste_items(p))
            
            # Donner le focus au frame pour les raccourcis
            grid_frame.bind("<Button-1>", lambda e: grid_frame.focus_set())
            
            # Configurer les colonnes
            grid_frame.grid_columnconfigure(0, weight=1, minsize=200)
            grid_frame.grid_columnconfigure(1, weight=0, minsize=50)
            
            # Trier et afficher les items
            items = player.get("m", {}).get("i", {}).get("i", [])
            sorted_items = self.get_sorted_items(items)
            self.display_items(grid_frame, sorted_items)
            
            # Configurer le scrolling
            items_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    def randomize_items(self):
        """Génère aléatoirement 10 items et les applique directement au fichier de sauvegarde."""
        if not self.saves or self.current_save_index is None:
            return

        # Vérifier que nous avons des items disponibles
        if not self.items_data:
            print("Tentative de rechargement du fichier items...")
            self.load_items_data()
            if not self.items_data:
                messagebox.showerror("Erreur", "Impossible de charger les items. Vérifiez que le fichier ItemName.json est présent et valide.")
                return

        filepath, save_data = self.saves[self.current_save_index]
        
        # Créer une copie de sauvegarde avant la modification
        backup_filepath = os.path.join(BACKUP_DIR, os.path.basename(filepath))
        shutil.copy(filepath, backup_filepath)
        
        # Générer 10 items aléatoires parmi les items disponibles dans le JSON
        available_items = list(self.items_data.keys())
        print(f"Nombre d'items disponibles: {len(available_items)}")
        if not available_items:
            messagebox.showerror("Erreur", "Aucun item trouvé dans le fichier ItemName.json")
            return
            
        for player in save_data.get("p", []):
            # Réinitialiser la liste des items
            new_items = []
            
            # Générer 10 items aléatoires
            for _ in range(10):
                item_id = random.choice(available_items)
                item_name = self.items_data[item_id]
                print(f"Ajout de l'item: {item_name} (ID: {item_id})")
                new_items.append({
                    "i": int(item_id),
                    "c": random.randint(1, 5)
                })
            
            # Mettre à jour les items du joueur
            if "m" in player and "i" in player["m"]:
                player["m"]["i"]["i"] = new_items
            else:
                print("Structure de données invalide pour le joueur:", player)
        
        # Sauvegarder les modifications
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=4)
        
        # Mettre à jour la liste des sauvegardes et rafraîchir l'affichage
        self.saves[self.current_save_index] = (filepath, save_data)
        self.refresh_save()
        messagebox.showinfo("Succès", "Les items ont été randomisés avec succès!")

    def refresh_save(self):
        """Recharge la save après un changement."""
        if not self.saves or self.current_save_index is None:
            return
        
        filepath, save_data = self.saves[self.current_save_index]
        with open(filepath, "r", encoding="utf-8") as f:
            save_data = json.load(f)
        
        self.saves[self.current_save_index] = (filepath, save_data)
        self.load_save()

    def update_file(self):
        """Met à jour la sauvegarde avec les nouvelles valeurs des items et du personnage."""
        if self.current_save_index is None:
            return
        
        filepath, save_data = self.saves[self.current_save_index]
        
        backup_filepath = os.path.join(BACKUP_DIR, os.path.basename(filepath))
        shutil.copy(filepath, backup_filepath)
        
        for player in save_data.get("p", []):
            player_id = player['si']['s']
            if player_id in self.character_entries:
                player["m"]["bn"] = self.character_entries[player_id].get()
            
            # Mettre à jour l'arsenal
            if player_id in self.arsenal_entries:
                arsenal = player.get("m", {}).get("l", {}).get("ml", [])
                for slot_index, entry in self.arsenal_entries[player_id]:
                    if slot_index < len(arsenal):
                        try:
                            new_value = entry.get().strip()
                            if new_value:  # Ne mettre à jour que si la valeur n'est pas vide
                                arsenal[slot_index]["bi"] = new_value
                        except ValueError:
                            pass  # Ignore les entrées invalides
            
            # Mettre à jour les items
            for item in player.get("m", {}).get("i", {}).get("i", []):
                if isinstance(item, dict) and "i" in item and "c" in item:
                    item_id = str(item["i"])
                    if item_id in self.entries:
                        try:
                            item["c"] = int(self.entries[item_id].get())
                        except ValueError:
                            pass  # Ignore les entrées invalides
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=4)
            
    def restore_backup(self):
        """Échange le fichier de sauvegarde actuel avec sa version de backup."""
        if self.current_save_index is None:
            return
            
        filepath, save_data = self.saves[self.current_save_index]
        filename = os.path.basename(filepath)
        backup_filepath = os.path.join(BACKUP_DIR, filename)
        
        if not os.path.exists(backup_filepath):
            messagebox.showerror("Erreur", "Aucune sauvegarde trouvée pour ce fichier.")
            return
            
        # Créer un fichier temporaire pour l'échange
        temp_filepath = os.path.join(BACKUP_DIR, f"temp_{filename}")
        
        try:
            # Déplacer le fichier actuel vers le fichier temporaire
            shutil.copy2(filepath, temp_filepath)
            # Déplacer la backup vers le fichier principal
            shutil.copy2(backup_filepath, filepath)
            # Déplacer le fichier temporaire vers la backup
            shutil.copy2(temp_filepath, backup_filepath)
            # Supprimer le fichier temporaire
            os.remove(temp_filepath)
            self.refresh_save()
        except Exception as e:
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)

    def show_items_menu(self, event, menu):
        """Affiche le menu contextuel des items."""
        menu.post(event.x_root, event.y_root)
        
    def copy_items(self, player, event=None):
        """Copie les items du joueur dans le presse-papier."""
        if "m" in player and "i" in player["m"] and "i" in player["m"]["i"]:
            self.clipboard_items = player["m"]["i"]["i"]
            messagebox.showinfo("Succès", "Items copiés avec succès!")
        
    def paste_items(self, player, event=None):
        """Colle les items du presse-papier au joueur."""
        if not self.clipboard_items:
            messagebox.showwarning("Attention", "Aucun item dans le presse-papier!")
            return
            
        if "m" in player and "i" in player["m"]:
            # Créer une copie profonde des items
            player["m"]["i"]["i"] = [item.copy() for item in self.clipboard_items]
            self.refresh_save()
            messagebox.showinfo("Succès", "Items collés avec succès!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ROR2SaveEditor(root)
    root.mainloop()
