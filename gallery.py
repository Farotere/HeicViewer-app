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
        
        # Appliquer le thème sombre à la fenêtre de recherche
        self.setStyleSheet("""
            QDialog {
                background-color: #232323;
            }
            QLabel {
                color: #E0E0E0;
                background-color: transparent;
            }
            QCheckBox {
                color: #E0E0E0;
                background-color: transparent;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                background-color: #4A4A4A;
                border: 1px solid #606060;
            }
            QCheckBox::indicator:checked {
                background-color: #5A5A5A;
                image: url(data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24"><path fill="white" d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/></svg>);
            }
            QPushButton {
                background-color: #353535;
                color: #E0E0E0;
                border: 1px solid #505050;
                border-radius: 4px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #454545;
            }
            QPushButton:pressed {
                background-color: #252525;
            }
            QScrollArea {
                background-color: #232323;
                border: 1px solid #363636;
            }
            QScrollArea > QWidget > QWidget {
                background-color: #232323;
            }
            QScrollBar {
                background-color: #2A2A2A;
                width: 12px;
                height: 12px;
            }
            QScrollBar::handle {
                background-color: #404040;
                border-radius: 4px;
            }
            QScrollBar::handle:hover {
                background-color: #505050;
            }
            QScrollBar::add-page, QScrollBar::sub-page {
                background-color: #2A2A2A;
            }
            QScrollBar::add-line, QScrollBar::sub-line {
                background-color: #2A2A2A;
            }
            QMessageBox {
                background-color: #303030;
            }
            QToolTip {
                background-color: #404040;
                color: #E0E0E0;
                border: 1px solid #505050;
            }
        """)
        
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Ajout d'un label d'information en haut
        info_frame = QFrame()
        info_frame.setFrameShape(QFrame.Shape.StyledPanel)
        info_frame.setStyleSheet("background-color: #404040; border: 1px solid #505050;")
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
        frame_layout.setContentsMargins(3, 3, 3, 3)
        frame_layout.setSpacing(2)
        
        # Définir le style de base du cadre
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setFrameShadow(QFrame.Shadow.Raised)
        frame.setLineWidth(1)
        
        # Ajouter un label pour le numéro
        num_label = QLabel(f"{index + 1}")
        num_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Créer le bouton pour l'image
        button = QPushButton()
        button.setToolTip(f"{index + 1} - {os.path.basename(image_path)}")
        button.setFixedSize(self.thumbnail_size, self.thumbnail_size)
        button.setFlat(True)  # Bouton plat pour un meilleur rendu visuel
        
        # Chargement et redimensionnement de la miniature
        try:
            _, pixmap = load_image(image_path, 70)  # Qualité réduite pour les miniatures
            pixmap = pixmap.scaled(
                QSize(self.thumbnail_size - 10, self.thumbnail_size - 10),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            button.setIcon(QIcon(pixmap))
            button.setIconSize(QSize(self.thumbnail_size - 12, self.thumbnail_size - 12))
            
            # Appliquer un style différent si c'est l'image courante
            if index == self.current_index:
                # Style pour l'image sélectionnée - conserve le gris sombre avec accent bleu
                frame.setStyleSheet("""
                    QFrame {
                        background-color: #383840;
                        border: 2px solid #6080B0;
                        border-radius: 6px;
                    }
                """)
                num_label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        color: #90A0D0;
                        font-size: 10pt;
                        background-color: #383840;
                    }
                """)
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #383840;
                        border: 1px solid #505060;
                        border-radius: 4px;
                    }
                    QPushButton:hover {
                        background-color: #404050;
                    }
                """)
            else:
                # Style normal - gris sombre
                frame.setStyleSheet("""
                    QFrame {
                        background-color: #404040;
                        border: 1px solid #505050;
                        border-radius: 4px;
                    }
                    QFrame:hover {
                        border: 1px solid #606060;
                        background-color: #454545;
                    }
                """)
                num_label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        color: #B0B0B0;
                        font-size: 9pt;
                        background-color: #404040;
                    }
                """)
                button.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border: 1px solid #505050;
                        border-radius: 2px;
                    }
                    QPushButton:hover {
                        background-color: #505050;
                        border: 1px solid #606060;
                    }
                """)
                
        except Exception as e:
            button.setText(os.path.basename(image_path))
        
        button.clicked.connect(lambda: self.select_image(image_path))
        
        frame_layout.addWidget(num_label)
        frame_layout.addWidget(button)
        
        return frame
    
    def select_image(self, image_path):
        """Sélectionne une image et ferme le dialogue"""
        self.selected_image_path = image_path
        self.accept()
    
    def on_close(self):
        """Gère la fermeture du dialogue en sauvegardant les images si demandé"""
        if self.save_checkbox.isChecked() and self.image_files:
            # Sauvegarder les images pour une utilisation future sans afficher de notification
            success = self.data_manager.add_search_result(self.image_files)
        self.reject()
