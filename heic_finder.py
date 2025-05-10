import os
import sys
import threading
import time
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
                           QTreeWidget, QTreeWidgetItem, QProgressBar, QFileDialog,
                           QMessageBox, QComboBox, QLineEdit, QCheckBox, QFrame)
from PyQt6.QtCore import Qt, QStandardPaths, pyqtSignal, QSize, QTimer
from PyQt6.QtGui import QIcon, QPixmap

from image_processing import load_image
from data_manager import HeicDataManager


class SearchResultItem(QTreeWidgetItem):
    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.file_path = path
        self.file_name = os.path.basename(path)
        self.file_size = os.path.getsize(path) / 1024  # Ko
        self.file_date = time.strftime('%d/%m/%Y %H:%M', 
                                       time.localtime(os.path.getmtime(path)))
        
        # Définition des colonnes pour l'affichage
        self.setText(0, self.file_name)
        self.setText(1, f"{self.file_size:.1f} Ko")
        self.setText(2, self.file_date)
        self.setText(3, os.path.dirname(path))
        
        # Charger une miniature en arrière-plan
        self.thumbnail_loaded = False


class HeicFinderDialog(QDialog):
    # Signaux pour la communication entre threads
    update_progress = pyqtSignal(int, str)
    search_completed = pyqtSignal(int)
    add_search_result = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Recherche de fichiers HEIC")
        self.setMinimumSize(900, 600)
        self.resize(1000, 700)
        
        self.parent_viewer = parent
        self.search_results = []
        self.search_thread = None
        self.is_searching = False
        self.thumbnail_size = 32
        self.save_results = True
        self.data_manager = HeicDataManager()
        
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
                background-color: #353535;
                border: 1px solid #505050;
            }
            QCheckBox::indicator:checked {
                background-color: #404060;
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
            QLineEdit {
                background-color: #353535;
                color: #E0E0E0;
                border: 1px solid #505050;
                border-radius: 3px;
                padding: 3px;
            }
            QComboBox {
                background-color: #353535;
                color: #E0E0E0;
                border: 1px solid #505050;
                border-radius: 3px;
                padding: 3px;
            }
            QComboBox::drop-down {
                background-color: #404040;
            }
            QComboBox::down-arrow {
                width: 14px;
                height: 14px;
            }
            QComboBox QAbstractItemView {
                background-color: #353535;
                color: #E0E0E0;
                border: 1px solid #505050;
                selection-background-color: #404050;
            }
            QFrame {
                background-color: #333333;
                border: 1px solid #404040;
            }
            QProgressBar {
                border: 1px solid #505050;
                background-color: #353535;
                text-align: center;
                color: #E0E0E0;
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background-color: #405060;
                width: 10px;
            }
            QTreeWidget {
                background-color: #303030;
                color: #E0E0E0;
                border: 1px solid #404040;
                alternate-background-color: #353535;
            }
            QTreeWidget::item:selected {
                background-color: #404050;
                color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #404040;
                color: #E0E0E0;
                border: 1px solid #505050;
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
            QToolTip {
                background-color: #404040;
                color: #E0E0E0;
                border: 1px solid #505050;
            }
        """)

        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        search_frame = QFrame()
        search_frame.setFrameShape(QFrame.Shape.StyledPanel)
        search_layout = QHBoxLayout(search_frame)
        
        self.location_combo = QComboBox()
        self.location_combo.addItem("Documents", QStandardPaths.StandardLocation.DocumentsLocation)
        self.location_combo.addItem("Images", QStandardPaths.StandardLocation.PicturesLocation)
        self.location_combo.addItem("Vidéos", QStandardPaths.StandardLocation.MoviesLocation)
        self.location_combo.addItem("Téléchargements", QStandardPaths.StandardLocation.DownloadLocation)
        self.location_combo.addItem("Bureau", QStandardPaths.StandardLocation.DesktopLocation)
        self.location_combo.addItem("Dossier personnel", QStandardPaths.StandardLocation.HomeLocation)
        self.location_combo.addItem("Disque principal", "root")
        self.location_combo.addItem("Personnalisé", "custom")
        
        self.search_path = QLineEdit()
        self.search_path.setReadOnly(False)
        self.search_path.setPlaceholderText("Saisissez ou sélectionnez un chemin de recherche...")
        self.browse_button = QPushButton("Parcourir...")
        self.browse_button.clicked.connect(self.browse_directory)
        
        self.recursive_check = QCheckBox("Recherche récursive")
        self.recursive_check.setChecked(True)
        
        self.search_button = QPushButton("Rechercher")
        self.search_button.clicked.connect(self.start_search)
        
        search_layout.addWidget(QLabel("Chercher dans:"))
        search_layout.addWidget(self.location_combo)
        search_layout.addWidget(self.search_path)
        search_layout.addWidget(self.browse_button)
        search_layout.addWidget(self.recursive_check)
        search_layout.addWidget(self.search_button)
        
        layout.addWidget(search_frame)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_label = QLabel("Prêt")
        
        progress_layout = QHBoxLayout()
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_label)
        layout.addLayout(progress_layout)
        self.result_tree = QTreeWidget()
        self.result_tree.setHeaderLabels(["Nom", "Taille", "Date", "Emplacement"])
        self.result_tree.setColumnWidth(0, 250)
        self.result_tree.setColumnWidth(1, 100)
        self.result_tree.setColumnWidth(2, 150)
        self.result_tree.setColumnWidth(3, 350)
        self.result_tree.setAlternatingRowColors(True)
        self.result_tree.itemDoubleClicked.connect(self.open_selected_file)
        layout.addWidget(self.result_tree)
        button_layout = QHBoxLayout()
        
        self.open_button = QPushButton("Ouvrir")
        self.open_button.clicked.connect(self.open_selected_file)
        self.cancel_button = QPushButton("Annuler recherche")
        self.cancel_button.clicked.connect(self.cancel_search)
        self.cancel_button.setEnabled(False)
        self.close_button = QPushButton("Fermer")
        self.close_button.clicked.connect(self.reject)
        self.save_results_check = QCheckBox("Utiliser ces résultats pour 'Voir tout'")
        self.save_results_check.setChecked(True)
        self.save_results_check.toggled.connect(self.toggle_save_results)
        
        button_layout.addWidget(self.open_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_results_check)
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
        self.location_combo.currentIndexChanged.connect(self.update_search_path)
        self.update_progress.connect(self.on_progress_update)
        self.search_completed.connect(self.on_search_completed)
        self.add_search_result.connect(self.on_result_found)
        self.update_search_path()
    
    def toggle_save_results(self, checked):
        self.save_results = checked
    
    def browse_directory(self):
        path = QFileDialog.getExistingDirectory(
            self, 
            "Choisir un dossier de recherche", 
            self.search_path.text() or QStandardPaths.writableLocation(QStandardPaths.StandardLocation.HomeLocation)
        )
        if path:
            self.search_path.setText(path)
            custom_index = self.location_combo.findData("custom")
            if custom_index >= 0:
                self.location_combo.setCurrentIndex(custom_index)
    
    def update_search_path(self):
        selection = self.location_combo.currentData()
        if selection == "custom":
            if not self.search_path.text() or self.sender() == self.location_combo:
                recent_searches = self.data_manager.get_recent_searches()
                if recent_searches:
                    self.search_path.setText(recent_searches[0])
                else:
                    self.browse_directory()
        elif selection == "root":
            if sys.platform == "win32":
                self.search_path.setText("C:\\")
            else:
                self.search_path.setText("/")
        else:
            self.search_path.setText(QStandardPaths.writableLocation(selection))
    
    def start_search(self):
        """Démarre la recherche avec le chemin actuellement saisi"""
        if self.is_searching:
            return
        search_path = self.search_path.text()
        if not search_path or not os.path.isdir(search_path):
            QMessageBox.warning(
                self,
                "Chemin invalide",
                "Le chemin de recherche spécifié n'existe pas ou n'est pas un dossier valide."
            )
            return
        self.is_searching = True
        self.search_results = []
        self.result_tree.clear()
        
        self.progress_bar.setValue(0)
        self.progress_label.setText("Recherche en cours...")
        
        self.search_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        
        recursive = self.recursive_check.isChecked()
        self.data_manager.save_recent_search(search_path)
        
        self.search_thread = threading.Thread(
            target=self.search_heic_files,
            args=(search_path, recursive)
        )
        self.search_thread.daemon = True
        self.search_thread.start()
    
    def cancel_search(self):
        if self.is_searching and self.search_thread:
            self.is_searching = False
            self.cancel_button.setEnabled(False)
            self.progress_label.setText("Annulation de la recherche...")
    
    def search_heic_files(self, root_path, recursive):
        try:
            file_count = 0
            total_files = 0

            if recursive:
                for root, _, files in os.walk(root_path):
                    total_files += len(files)
            else:
                total_files = len(os.listdir(root_path))
            if recursive:
                for root, _, files in os.walk(root_path):
                    if not self.is_searching:
                        break
                        
                    for file in files:
                        if not self.is_searching:
                            break
                            
                        file_count += 1
                        if file_count % 50 == 0:
                            progress = int((file_count / total_files) * 100) if total_files else 0
                            self.update_progress.emit(progress, f"Recherche: {file_count}/{total_files} fichiers examinés")
                        
                        if file.lower().endswith(('.heic', '.heif')):
                            full_path = os.path.join(root, file)
                            self.add_search_result.emit(full_path)
            else:
                for item in os.listdir(root_path):
                    if not self.is_searching:
                        break
                        
                    file_count += 1
                    if file_count % 50 == 0:
                        progress = int((file_count / total_files) * 100) if total_files else 0
                        self.update_progress.emit(progress, f"Recherche: {file_count}/{total_files} fichiers examinés")
                    
                    full_path = os.path.join(root_path, item)
                    if os.path.isfile(full_path) and item.lower().endswith(('.heic', '.heif')):
                        self.add_search_result.emit(full_path)
            self.search_completed.emit(len(self.search_results))
            
        except Exception as e:
            self.update_progress.emit(0, f"Erreur: {str(e)}")
            self.search_completed.emit(-1)
    
    def on_progress_update(self, progress, message):
        self.progress_bar.setValue(progress)
        self.progress_label.setText(message)
    
    def on_result_found(self, file_path):
        self.search_results.append(file_path)
        item = SearchResultItem(file_path)
        self.result_tree.addTopLevelItem(item)
        QTimer.singleShot(10, lambda: self.load_thumbnail_for_item(item))
    
    def load_thumbnail_for_item(self, item):
        try:
            if not hasattr(item, 'thumbnail_loaded') or item.thumbnail_loaded:
                return
                
            _, pixmap = load_image(item.file_path, 50)
            if pixmap:
                icon_pixmap = pixmap.scaled(QSize(self.thumbnail_size, self.thumbnail_size), 
                                           Qt.AspectRatioMode.KeepAspectRatio,
                                           Qt.TransformationMode.SmoothTransformation)
                item.setIcon(0, QIcon(icon_pixmap))
                item.thumbnail_loaded = True
        except:
            pass
    
    def on_search_completed(self, count):
        self.is_searching = False
        self.search_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        
        if count >= 0:
            self.progress_bar.setValue(100)
            self.progress_label.setText(f"Recherche terminée. {count} fichiers HEIC trouvés.")
            
            if self.save_results and count > 0:
                self.data_manager.add_search_result(self.search_results)
        else:
            self.progress_bar.setValue(0)
            self.progress_label.setText("Recherche échouée.")
    
    def open_selected_file(self):
        selected_items = self.result_tree.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Sélection", "Veuillez sélectionner une image à ouvrir.")
            return
            
        item = selected_items[0]
        if hasattr(item, 'file_path') and os.path.isfile(item.file_path):
            if self.save_results and self.parent_viewer and self.search_results:
                self.parent_viewer.set_search_results(self.search_results)
            
            self.accept()
            if self.parent_viewer:
                self.parent_viewer.open_heic_file(item.file_path)

    def accept(self):
        if self.save_results and self.parent_viewer and self.search_results:
            self.parent_viewer.set_search_results(self.search_results)
        super().accept()

def show_heic_finder(parent_window):
    finder = HeicFinderDialog(parent_window)
    finder.exec()
