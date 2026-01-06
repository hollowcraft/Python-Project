import tkinter as tk
from tkinter import ttk
import ollama 
import os
from datetime import datetime

class OllamaManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Ollama Manager")
        self.master.geometry("800x600")
        self.font_size = 10  # Default font size

        # Créer le panneau principal
        self.main_panel = ttk.PanedWindow(master, orient=tk.HORIZONTAL)
        self.main_panel.pack(fill=tk.BOTH, expand=True)

        # Panneau gauche pour la liste des modèles
        self.left_frame = ttk.Frame(self.main_panel)
        self.main_panel.add(self.left_frame)

        # Liste des modèles
        self.model_label = ttk.Label(self.left_frame, text="Available Models")
        self.model_label.pack(pady=5, padx=5)

        # Créer la liste avec scrollbar
        self.model_listbox = tk.Listbox(self.left_frame, width=30)
        self.scrollbar = ttk.Scrollbar(self.left_frame, orient="vertical")
        self.model_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.model_listbox.yview)

        self.model_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Ajoutez des modèles statiques
        self.model_listbox.insert(tk.END, "gemma3:1b")
        self.model_listbox.insert(tk.END, "codellama:latest")

        # Après la liste des modèles, ajoutons une liste pour les chats
        self.chats_label = ttk.Label(self.left_frame, text="Chat History")
        self.chats_label.pack(pady=5, padx=5)

        # Créer la liste des chats avec scrollbar
        self.chats_listbox = tk.Listbox(self.left_frame, width=30)
        self.chats_scrollbar = ttk.Scrollbar(self.left_frame, orient="vertical")
        self.chats_listbox.config(yscrollcommand=self.chats_scrollbar.set)
        self.chats_scrollbar.config(command=self.chats_listbox.yview)

        self.chats_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.chats_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Ajoutez des chats statiques
        self.chats_listbox.insert(tk.END, "2025-04-21 16:04")
        self.chats_listbox.insert(tk.END, "2025-04-21 16:10")

        # Bind la sélection d'un modèle pour mettre à jour la liste des chats
        self.model_listbox.bind('<<ListboxSelect>>', self.update_chat_list)

        # Bind la sélection d'un chat pour charger son contenu
        self.chats_listbox.bind('<Double-Button-1>', self.load_chat_content)

        # Panneau droit pour les actions et le chat
        self.right_frame = ttk.Frame(self.main_panel)
        self.main_panel.add(self.right_frame)

        # Zone de chat
        self.chat_frame = ttk.Frame(self.right_frame)
        self.chat_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Zone de texte pour afficher les messages avec style
        self.chat_text = tk.Text(self.chat_frame, wrap=tk.WORD, height=20, font=('Segoe UI', self.font_size))
        self.chat_text.tag_configure('user', background='#F7F7F8', font=('Segoe UI', self.font_size))
        self.chat_text.tag_configure('assistant', background='white', font=('Segoe UI', self.font_size))
        self.chat_scroll = ttk.Scrollbar(self.chat_frame, command=self.chat_text.yview)
        self.chat_text.configure(yscrollcommand=self.chat_scroll.set)
        
        self.chat_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.chat_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Zone de saisie en bas
        self.input_frame = ttk.Frame(self.right_frame)
        self.input_frame.pack(fill=tk.X, padx=5, pady=5)

        # Zone de saisie avec bordure
        self.input_text = tk.Text(self.input_frame, height=3, wrap=tk.WORD, font=('Segoe UI', 10))
        self.input_text.pack(fill=tk.X, pady=(0, 5))
        
        # Bouton d'envoi
        self.send_btn = ttk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_btn.pack(side=tk.RIGHT)

        # Boutons en bas à gauche
        self.buttons_frame = ttk.Frame(self.input_frame)
        self.buttons_frame.pack(side=tk.LEFT, padx=5)
        
        self.settings_btn = ttk.Button(self.buttons_frame, text="⚙️", width=3, command=self.show_settings)
        self.settings_btn.pack(side=tk.LEFT)

        # Bind Enter key to send message
        self.input_text.bind('<Return>', lambda e: self.send_message() if not e.state & 0x1 else None)
        self.input_text.bind('<Shift-Return>', lambda e: self.input_text.insert(tk.END, '\n'))

        # Charger la liste des modèles
        self.load_models()

    def load_models(self):
        try:
            response = ollama.list()
            # Clear existing items
            self.model_listbox.delete(0, tk.END)
            
            # Extract models from response
            if hasattr(response, 'models'):
                models = response.models
            else:
                models = response
                
            # Add each model to the listbox
            for model in models:
                if hasattr(model, 'model'):
                    self.model_listbox.insert(tk.END, model.model)
                else:
                    self.model_listbox.insert(tk.END, str(model))
                    
        except Exception as e:
            print(f"Error loading models: {e}")

    def create_chat_directory(self, model_name):
        base_dir = os.path.join(os.getcwd(), "Ollama Manager/chats")
        model_dir = os.path.join(base_dir, model_name.replace(':', '_'))
        
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
            
        # Créer un nouveau fichier de chat avec la date
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        chat_file = os.path.join(model_dir, f"chat_{timestamp}.txt")
        return chat_file

    def start_chat(self):
        selection = self.model_listbox.curselection()
        if selection:
            selected_model = self.model_listbox.get(selection[0])
            try:
                # Créer le dossier pour le chat
                chat_file = self.create_chat_directory(selected_model)
                
                # Effacer le contenu précédent
                self.chat_text.delete('1.0', tk.END)
                
                # Initialize chat with the selected model
                response = ollama.chat(
                    model=selected_model,
                    messages=[{
                        'role': 'system',
                        'content': 'You are a helpful assistant.'
                    }]
                )
                
                # Afficher la réponse dans l'interface
                response_content = response['message']['content']
                self.chat_text.insert(tk.END, f"Assistant: {response_content}\n\n", 'assistant')
                
                # Sauvegarder dans le fichier (sans le nom du modèle)
                with open(chat_file, 'w', encoding='utf-8') as f:
                    f.write(f"Assistant: {response_content}\n")
                
            except Exception as e:
                error_msg = f"Error starting chat: {e}"
                print(error_msg)
                self.chat_text.insert(tk.END, f"Error: {error_msg}\n", 'error')

    def send_message(self):
        message = self.input_text.get('1.0', tk.END).strip()
        if not message:
            return
        
        selection = self.model_listbox.curselection()
        if selection:
            selected_model = self.model_listbox.get(selection[0])
            try:
                # Afficher le message utilisateur (sans le préfixe)
                self.chat_text.delete('1.0', tk.END)
                self.chat_text.insert(tk.END, "Test message\n\n", 'user')
                self.chat_text.update_idletasks()
                
                self.chat_text.insert(tk.END, f"\n{message}\n\n", 'user')
                self.chat_text.see(tk.END)
                
                # Effacer la zone de saisie
                self.input_text.delete('1.0', tk.END)
                
                # Envoyer au modèle
                response = ollama.chat(
                    model=selected_model,
                    messages=[{
                        'role': 'user',
                        'content': message
                    }]
                )
                
                # Afficher la réponse (sans le préfixe)
                response_content = response['message']['content']
                self.chat_text.insert(tk.END, f"{response_content}\n\n", 'assistant')
                self.chat_text.see(tk.END)
                
                # Sauvegarder dans le fichier (avec les préfixes)
                chat_file = self.create_chat_directory(selected_model)
                with open(chat_file, 'a', encoding='utf-8') as f:
                    f.write(f"User: {message}\n")
                    f.write(f"Assistant: {response_content}\n\n")
                
            except Exception as e:
                error_msg = f"Error: {e}"
                self.chat_text.insert(tk.END, f"{error_msg}\n", 'error')
                self.chat_text.see(tk.END)

    def show_settings(self):
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Settings")
        settings_window.geometry("300x200")
        
        # Font size settings
        font_frame = ttk.LabelFrame(settings_window, text="Font Size")
        font_frame.pack(padx=10, pady=10, fill=tk.X)
        
        font_size = ttk.Scale(
            font_frame, 
            from_=8, 
            to=24, 
            orient=tk.HORIZONTAL, 
            value=self.font_size,
            command=self.update_font_size
        )
        font_size.pack(padx=10, pady=10, fill=tk.X)
        
        size_label = ttk.Label(font_frame, text=f"Current size: {self.font_size}")
        size_label.pack(pady=5)
        
        # Update label when scale moves
        def update_label(event):
            size_label.config(text=f"Current size: {int(font_size.get())}")
        font_size.bind("<Motion>", update_label)

    def update_font_size(self, size):
        self.font_size = int(float(size))
        self.chat_text.configure(font=('Segoe UI', self.font_size))
        self.chat_text.tag_configure('user', font=('Segoe UI', self.font_size))
        self.chat_text.tag_configure('assistant', font=('Segoe UI', self.font_size))

    def update_chat_list(self, event=None):
        selection = self.model_listbox.curselection()
        print(f"update_chat_list triggered. Selection: {selection}")  # Debug
        if not selection:
            print("No model selected in update_chat_list.")  # Debug
            return  # Ignore si aucune sélection n'est faite
        
        selected_model = self.model_listbox.get(selection[0])
        print(f"Model selected: {selected_model}")  # Debug
        self.load_chat_history(selected_model)

    def load_chat_history(self, model_name):
        print(f"Loading chat history for model: {model_name}")  # Debug
        self.chats_listbox.delete(0, tk.END)  # Clear existing items
        
        # Construit le chemin du dossier du modèle
        base_dir = os.path.join(os.getcwd(), "Ollama Manager/chats")
        model_dir = os.path.join(base_dir, model_name.replace(':', '_'))
        
        if os.path.exists(model_dir):
            # Liste tous les fichiers de chat dans le dossier
            chat_files = sorted([f for f in os.listdir(model_dir) if f.startswith('chat_')])
            
            for chat_file in chat_files:
                # Convertit le nom du fichier en format lisible
                timestamp = chat_file[5:-4]  # Enlève 'chat_' et '.txt'
                try:
                    date_obj = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
                    display_date = date_obj.strftime("%Y-%m-%d %H:%M")
                    self.chats_listbox.insert(tk.END, display_date)
                except:
                    self.chats_listbox.insert(tk.END, chat_file)
        else:
            print(f"No chat directory found for model: {model_name}")  # Debug

    def load_chat_content(self, event=None):
        model_selection = self.model_listbox.curselection()
        chat_selection = self.chats_listbox.curselection()
        
        print(f"load_chat_content triggered. Model selection: {model_selection}, Chat selection: {chat_selection}")  # Debug
        
        if not model_selection:
            print("No model selected.")  # Debug
            return
        if not chat_selection:
            print("No chat selected.")  # Debug
            return
        
        selected_model = self.model_listbox.get(model_selection[0])
        selected_chat = self.chats_listbox.get(chat_selection[0])
        
        print(f"Selected model: {selected_model}")  # Debug
        print(f"Selected chat: {selected_chat}")    # Debug
        
        # Construit le chemin du fichier
        base_dir = os.path.join(os.getcwd(), "Ollama Manager", "chats")
        model_dir = os.path.join(base_dir, selected_model.replace(':', '_'))
        
        try:
            date_obj = datetime.strptime(selected_chat, "%Y-%m-%d %H:%M")
            file_timestamp = date_obj.strftime("%Y%m%d_%H%M%S")
            chat_file = f"chat_{file_timestamp}.txt"
            file_path = os.path.join(model_dir, chat_file)
            
            print(f"Looking for file: {file_path}")  # Debug
            
            if os.path.exists(file_path):
                print(f"File found!")  # Debug
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(f"Content read: {content}")  # Debug
                    
                    # Clear existing content
                    self.chat_text.delete('1.0', tk.END)
                    
                    # Process the content line by line
                    lines = content.strip().split('\n')
                    for line in lines:
                        line = line.strip()
                        if not line:  # Skip empty lines
                            continue
                            
                        if line.startswith('User: '):
                            msg = line[6:]
                            print(f"User message: {msg}")  # Debug
                            self.chat_text.insert(tk.END, f"{msg}\n\n", 'user')
                        elif line.startswith('Assistant: '):
                            msg = line[11:]
                            print(f"Assistant message: {msg}")  # Debug
                            self.chat_text.insert(tk.END, f"{msg}\n\n", 'assistant')
                    
                    # Forcer la mise à jour de l'interface
                    self.chat_text.update_idletasks()
                    self.chat_text.see('1.0')
            else:
                print(f"File not found: {file_path}")  # Debug
                
        except Exception as e:
            print(f"Error loading chat: {e}")
            import traceback
            traceback.print_exc()  # This will print the full error stack

if __name__ == "__main__":
    root = tk.Tk()
    app = OllamaManager(root)
    root.mainloop()




