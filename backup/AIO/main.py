from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json
import os
import subprocess

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mon Application")
        self.setGeometry(100, 100, 1200, 800)
        
        # Widget principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Layout horizontal principal
        layout = QHBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Panneau de gauche (style Discord)
        self.sidebar = QWidget()
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(8, 8, 8, 8)
        sidebar_layout.setSpacing(8)
        self.sidebar.setFixedWidth(90)
        self.sidebar.setStyleSheet("background-color: #2F3136; padding: 0;")
        
        # Panneau de droite
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background-color: #36393F;")
        self.content_layout = QVBoxLayout(self.content_widget)
        
        # Dictionnaire pour stocker les widgets de contenu de chaque onglet
        self.tab_contents = {}
        
        # Liste des onglets avec menu contextuel
        self.tabs_list = QListWidget()
        self.tabs_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabs_list.customContextMenuRequested.connect(self.show_tab_context_menu)
        self.tabs_list.setDragDropMode(QAbstractItemView.InternalMove)
        self.tabs_list.setViewMode(QListView.ListMode)
        self.tabs_list.setIconSize(QSize(48, 192))
        self.tabs_list.setSpacing(4)
        self.tabs_list.setStyleSheet("""
            QListWidget {
                background-color: #2F3136;
                color: transparent;  /* Cache le texte */
                border: none;
                padding: 4px;
            }
            QListWidget::item {
                background-color: #36393F;
                border-radius: 24px;  /* Rend les items parfaitement ronds */
                margin-bottom: 4px;
                height: 48px;  /* Même hauteur que l'icône */
                width: 48px;  /* Même largeur que l'icône */
            }
            QListWidget::item:hover {
                background-color: #404EED;
            }
            QListWidget::item:selected {
                background-color: #5865F2;
            }
        """)
        
        # Bouton pour ajouter un nouvel onglet
        add_tab_button = QPushButton("+")
        add_tab_button.setFixedSize(48, 48)
        add_tab_button.setStyleSheet("""
            QPushButton {
                background-color: #404EED;
                color: white;
                border-radius: 24px;
                font-size: 24px;
                font-weight: bold;
                padding: 0;
                margin: 4px;
            }
            QPushButton:hover {
                background-color: #5865F2;
            }
        """)
        add_tab_button.clicked.connect(self.create_new_tab)
        
        # Ajout des widgets à la barre latérale
        sidebar_layout.addWidget(self.tabs_list, 1)  # Le 1 permet l'expansion verticale
        sidebar_layout.addWidget(add_tab_button, 0, Qt.AlignCenter)  # Centré en bas
        
        # Charger les onglets existants
        self.load_tabs()

        # Connecter le signal de sélection d'onglet
        self.tabs_list.itemClicked.connect(self.show_tab_content)

        # Ajout direct des widgets au layout principal
        layout.addWidget(self.sidebar)
        layout.addWidget(self.content_widget, 1)  # Le 1 permet l'expansion

    def create_new_tab(self):
        dialog = NewTabDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            tab_data = {
                "name": dialog.name_input.text(),
                "image_path": dialog.image_path,
                "buttons": [],
                "code_blocks": []
            }
            self.add_tab(tab_data)
            self.save_tabs()

    def add_tab(self, tab_data):
        item = QListWidgetItem(tab_data["name"])  # Le nom est toujours stocké mais pas affiché
        if tab_data["image_path"]:
            icon = QIcon(tab_data["image_path"])
        else:
            # Créer une icône par défaut avec les initiales du nom
            initials = ''.join(word[0].upper() for word in tab_data["name"].split()[:2])
            pixmap = QPixmap(48, 48)
            pixmap.fill(QColor("#404EED"))
            painter = QPainter(pixmap)
            painter.setPen(QColor("white"))
            painter.setFont(QFont("Arial", 16, QFont.Bold))
            painter.drawText(pixmap.rect(), Qt.AlignCenter, initials)
            painter.end()
            icon = QIcon(pixmap)
            
        item.setIcon(icon)
        item.setData(Qt.UserRole, tab_data["image_path"])
        item.setSizeHint(QSize(48, 48))  # Taille fixe pour les items
        self.tabs_list.addItem(item)

        # Connecter le signal de fin de glisser-déposer pour sauvegarder l'ordre
        self.tabs_list.model().rowsMoved.connect(self.save_tabs)

    def save_tabs(self):
        tabs = []
        for i in range(self.tabs_list.count()):
            item = self.tabs_list.item(i)
            tabs.append({
                "name": item.text(),
                "image_path": item.data(Qt.UserRole) if item.data(Qt.UserRole) else ""
            })
        with open("tabs.json", "w") as f:
            json.dump(tabs, f)

    def load_tabs(self):
        if os.path.exists("tabs.json"):
            with open("tabs.json", "r") as f:
                tabs = json.load(f)
                for tab in tabs:
                    self.add_tab(tab)

    def show_tab_context_menu(self, position):
        item = self.tabs_list.itemAt(position)
        if item is None:
            return
            
        menu = QMenu()
        edit_action = menu.addAction("Modifier")
        delete_action = menu.addAction("Supprimer")
        
        # Style du menu contextuel
        menu.setStyleSheet("""
            QMenu {
                background-color: #18191c;
                color: #dcddde;
                border: 1px solid #2f3136;
                border-radius: 4px;
            }
            QMenu::item {
                padding: 8px 24px;
            }
            QMenu::item:selected {
                background-color: #404EED;
            }
        """)
        
        action = menu.exec_(self.tabs_list.mapToGlobal(position))
        
        if action == edit_action:
            self.edit_tab(item)
        elif action == delete_action:
            self.delete_tab(item)

    def edit_tab(self, item):
        dialog = NewTabDialog(self)
        dialog.name_input.setText(item.text())
        if item.data(Qt.UserRole):
            dialog.image_path = item.data(Qt.UserRole)
            
        if dialog.exec_() == QDialog.Accepted:
            item.setText(dialog.name_input.text())
            if dialog.image_path:
                icon = QIcon(dialog.image_path)
                item.setIcon(icon)
                item.setData(Qt.UserRole, dialog.image_path)
            self.save_tabs()

    def delete_tab(self, item):
        confirm = QMessageBox()
        confirm.setStyleSheet("""
            QMessageBox {
                background-color: #36393F;
                color: white;
            }
            QPushButton {
                background-color: #404EED;
                color: white;
                border-radius: 4px;
                padding: 6px 12px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #5865F2;
            }
        """)
        confirm.setWindowTitle("Confirmation")
        confirm.setText(f"Voulez-vous vraiment supprimer l'onglet '{item.text()}' ?")
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setDefaultButton(QMessageBox.No)
        
        if confirm.exec_() == QMessageBox.Yes:
            self.tabs_list.takeItem(self.tabs_list.row(item))
            self.save_tabs()

    def show_tab_content(self, item):
        # Cacher tous les contenus
        for content in self.tab_contents.values():
            content.hide()
        
        # Afficher le contenu de l'onglet sélectionné
        if item.text() in self.tab_contents:
            self.tab_contents[item.text()].show()
        else:
            # Créer un nouveau widget de contenu
            content_widget = TabContentWidget(self, item.text())
            self.tab_contents[item.text()] = content_widget
            self.content_layout.addWidget(content_widget)
            content_widget.show()

class NewTabDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nouvel onglet")
        self.image_path = ""
        
        layout = QVBoxLayout(self)
        
        # Champ pour le nom
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nom de l'onglet")
        layout.addWidget(self.name_input)
        
        # Bouton pour choisir une image
        image_button = QPushButton("Choisir une image")
        image_button.clicked.connect(self.choose_image)
        layout.addWidget(image_button)
        
        # Boutons de validation
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def choose_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Choisir une image",
            "",
            "Images (*.png *.jpg *.jpeg *.gif)"
        )
        if file_name:
            self.image_path = file_name

class TabContentWidget(QWidget):
    def __init__(self, parent, tab_name):
        super().__init__(parent)
        self.tab_name = tab_name
        self.setup_ui()
        self.setStyleSheet("""
            QWidget {
                background-color: #36393F;
                color: white;
            }
        """)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Barre d'outils
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(10, 10, 10, 10)
        toolbar.setStyleSheet("""
            QWidget {
                background-color: #2F3136;
                border-radius: 8px;
                min-height: 50px;
            }
        """)
        
        # Bouton pour ajouter un bouton
        add_button = QPushButton("Ajouter un bouton")
        add_button.clicked.connect(self.add_button)
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #404EED;
                color: white;
                border-radius: 4px;
                padding: 8px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #5865F2;
            }
        """)
        
        toolbar_layout.addWidget(add_button)
        toolbar_layout.addStretch()
        
        # Zone de contenu scrollable
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #36393F;
            }
            QScrollBar:vertical {
                background-color: #2F3136;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background-color: #202225;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #404EED;
            }
        """)
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setAlignment(Qt.AlignTop)
        self.content_layout.setSpacing(10)
        self.content_widget.setStyleSheet("background-color: #36393F;")
        
        scroll.setWidget(self.content_widget)
        
        layout.addWidget(toolbar)
        layout.addWidget(scroll)

    def add_button(self):
        dialog = ButtonDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Créer un widget conteneur pour le bouton
            button_container = QWidget()
            container_layout = QVBoxLayout(button_container)
            container_layout.setContentsMargins(0, 0, 0, 0)
            
            # Créer le bouton carré
            button = QPushButton()
            button.setFixedSize(48, 48)  # Même taille que les onglets
            button.setToolTip(dialog.name_input.text())  # Afficher le nom en tooltip
            
            # Créer une icône avec les initiales du nom
            initials = ''.join(word[0].upper() for word in dialog.name_input.text().split()[:2])
            pixmap = QPixmap(48, 48)
            pixmap.fill(QColor("#2F3136"))
            painter = QPainter(pixmap)
            painter.setPen(QColor("white"))
            painter.setFont(QFont("Arial", 16, QFont.Bold))
            painter.drawText(pixmap.rect(), Qt.AlignCenter, initials)
            painter.end()
            
            button.setIcon(QIcon(pixmap))
            button.setIconSize(QSize(48, 48))
            
            button.setStyleSheet("""
                QPushButton {
                    background-color: #2F3136;
                    border-radius: 24px;
                    padding: 0;
                    margin: 4px;
                }
                QPushButton:hover {
                    background-color: #404EED;
                }
            """)
            
            # Stocker le code dans les données du bouton
            button.setProperty("code", dialog.code_input.toPlainText())
            button.clicked.connect(lambda: self.execute_command(button.property("code")))
            
            container_layout.addWidget(button)
            self.content_layout.insertWidget(self.content_layout.count(), button_container)

    def execute_command(self, command):
        try:
            subprocess.Popen(command, shell=True)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

class ButtonDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nouveau bouton")
        self.setStyleSheet("""
            QDialog {
                background-color: #36393F;
                color: white;
            }
            QLineEdit, QTextEdit {
                background-color: #2F3136;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
            }
            QPushButton {
                background-color: #404EED;
                color: white;
                border-radius: 4px;
                padding: 8px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #5865F2;
            }
            QLabel {
                color: white;
            }
        """)
        layout = QVBoxLayout(self)
        
        # Nom du bouton
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nom du bouton")
        
        # Code à exécuter
        self.code_input = QTextEdit()
        self.code_input.setPlaceholderText("Code à exécuter")
        self.code_input.setMinimumHeight(100)
        
        # Boutons de validation
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addWidget(QLabel("Nom du bouton:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Code:"))
        layout.addWidget(self.code_input)
        layout.addWidget(buttons)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
