import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                            QScrollArea, QLabel, QGridLayout, QCheckBox,
                            QMessageBox, QFrame)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QIcon

from image_processing import load_image
from data_manager import HeicDataManager

class ImageGalleryDialog(QDialog):
    """Dialogue affichant une galerie de toutes les images disponibles"""
    
    def __init__(self, parent, image_files, current_index):
        super().__init__(parent)
        self.setWindowTitle("Galerie d'images")
        self.setMinimumSize(800, 600)
        
        self.image_files = image_files
        self.current_index = current_index
        self.selected_image_path = None
        self.thumbnail_size = 150
        self.data_manager = HeicDataManager()
        
        # Mettre à jour le titre avec le nombre d'images
        self.setWindowTitle(f"Galerie d'images - {len(image_files)} images")
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Ajout d'un label d'information en haut
        info_frame = QFrame()
        info_frame.setFrameShape(QFrame.Shape.StyledPanel)
        info_layout = QHBoxLayout(info_frame)
        
        if self.current_index >= 0 and self.current_index < len(self.image_files):
            current_file = os.path.basename(self.image_files[self.current_index])
            info_label = QLabel(f"Image courante: {self.current_index + 1}/{len(self.image_files)} - {current_file}")
        else:
            info_label = QLabel(f"Total: {len(self.image_files)} images")
        
        info_layout.addWidget(info_label)
        layout.addWidget(info_frame)
        
        # Création de la grille pour les miniatures
        self.grid_layout = QGridLayout()
        
        # Nombre de colonnes en fonction de la largeur
        num_columns = max(3, self.width() // (self.thumbnail_size + 10))
        
        # Chargement des miniatures
        for i, image_path in enumerate(self.image_files):
            item = self.create_thumbnail_widget(image_path, i)
            row = i // num_columns
            col = i % num_columns
            self.grid_layout.addWidget(item, row, col)
        
        # Conteneur pour la grille avec défilement
        container = QLabel()
        container.setLayout(self.grid_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidget(container)
        scroll_area.setWidgetResizable(True)
        
        layout.addWidget(scroll_area)
        
        # Boutons de navigation
        button_layout = QHBoxLayout()
        
        # Nouvelle case à cocher pour sauvegarder la liste
        self.save_checkbox = QCheckBox("Enregistrer ces images pour les sessions futures")
        self.save_checkbox.setChecked(True)
        button_layout.addWidget(self.save_checkbox)
        
        button_layout.addStretch()
        
        close_button = QPushButton("Fermer")
        close_button.clicked.connect(self.on_close)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        
        # Si une image courante est définie, faire défiler jusqu'à elle
        if self.current_index >= 0:
            QTimer.singleShot(100, self.scroll_to_current)
        
    def scroll_to_current(self):
        """Fait défiler la vue jusqu'à l'image courante"""
        if self.current_index >= 0 and hasattr(self, 'container'):
            # La logique pour faire défiler jusqu'à l'élément actuel
            pass
        
    def create_thumbnail_widget(self, image_path, index):
        """Crée un widget miniature pour une image"""
        # Créer un conteneur pour la miniature et son numéro
        frame = QFrame()
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(2, 2, 2, 2)
        
        # Ajouter un label pour le numéro
        num_label = QLabel(f"{index + 1}")
        num_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        num_label.setStyleSheet("font-weight: bold;")
        frame_layout.addWidget(num_label)
        
        # Créer le bouton pour l'image
        button = QPushButton()
        button.setToolTip(f"{index + 1} - {os.path.basename(image_path)}")
        button.setFixedSize(self.thumbnail_size, self.thumbnail_size)
        
        # Chargement et redimensionnement de la miniature
        try:
            _, pixmap = load_image(image_path, 70)  # Qualité réduite pour les miniatures
            pixmap = pixmap.scaled(
                QSize(self.thumbnail_size - 10, self.thumbnail_size - 10),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            button.setIcon(QIcon(pixmap))
            button.setIconSize(QSize(self.thumbnail_size - 10, self.thumbnail_size - 10))
            if index == self.current_index:
                button.setStyleSheet("border: 3px solid blue; background-color: #E0E0FF;")
                frame.setStyleSheet("background-color: #E0E0FF;")
                
        except Exception as e:
            button.setText(os.path.basename(image_path))
        button.clicked.connect(lambda: self.select_image(image_path))
        
        frame_layout.addWidget(button)
        
        return frame
    
    def select_image(self, image_path):
        """Sélectionne une image et ferme le dialogue"""
        self.selected_image_path = image_path
        self.accept()
    
    def on_close(self):
        """Gère la fermeture du dialogue en sauvegardant les images si demandé"""
        if self.save_checkbox.isChecked() and self.image_files:
            # Sauvegarder les images pour une utilisation future
            success = self.data_manager.add_search_result(self.image_files)
            if success and len(self.image_files) > 5:  # Notification seulement si nombre significatif
                QMessageBox.information(
                    self, 
                    "Images sauvegardées", 
                    f"{len(self.image_files)} images ont été sauvegardées et seront disponibles lors de la prochaine ouverture."
                )
        self.reject()
