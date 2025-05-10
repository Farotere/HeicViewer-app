import os
import sys
from PyQt6.QtWidgets import (QMainWindow, QLabel, QScrollArea, 
                            QStatusBar, QMessageBox, QFileDialog,
                            QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                            QListWidget, QListWidgetItem, QGridLayout)
from PyQt6.QtCore import Qt, QStandardPaths, QPoint, QSize
from PyQt6.QtGui import QPixmap, QKeySequence, QShortcut, QIcon

from ui_components import create_menu, create_toolbar
from image_processing import load_image
from utils import show_about_dialog, show_association_dialog, create_file_association
from gallery import ImageGalleryDialog
from heic_finder import show_heic_finder as show_finder_dialog
from data_manager import HeicDataManager
from viewer_utils import get_relative_position, adjust_scroll_position

class HeicViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.current_image = None
        self.current_file_path = None
        self.current_pixmap = None
        self.is_fit_to_window = True
        self.jpeg_quality = 100
        self.zoom_factor = 1.2
        self.current_scale = 1.0
        self.image_files = []
        self.search_results = []
        self.current_index = -1
        self.using_search_results = False
        self.data_manager = HeicDataManager()
        
        # Appliquer le thème sombre à l'application principale
        self.setStyleSheet("""
            QMainWindow {
                background-color: #232323;
            }
            QLabel {
                color: #E0E0E0;
                background-color: transparent;
            }
            QStatusBar {
                background-color: #303030;
                color: #E0E0E0;
                border-top: 1px solid #404040;
            }
            QMenuBar {
                background-color: #303030;
                color: #E0E0E0;
                border-bottom: 1px solid #404040;
            }
            QMenuBar::item {
                background-color: #303030;
                color: #E0E0E0;
            }
            QMenuBar::item:selected {
                background-color: #404050;
            }
            QMenu {
                background-color: #303030;
                color: #E0E0E0;
                border: 1px solid #404040;
            }
            QMenu::item:selected {
                background-color: #404050;
            }
            QToolBar {
                background-color: #303030;
                border: 1px solid #404040;
            }
            QToolButton {
                background-color: #303030;
                color: #E0E0E0;
                border: 1px solid #303030;
                border-radius: 2px;
                padding: 3px;
            }
            QToolButton:hover {
                background-color: #404040;
                border: 1px solid #505050;
            }
            QToolButton:pressed {
                background-color: #252525;
            }
            QScrollArea {
                background-color: #232323;
                border: 1px solid #363636;
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
            QFileDialog {
                background-color: #303030;
                color: #E0E0E0;
            }
            QHeaderView::section {
                background-color: #404040;
                color: #E0E0E0;
                border: 1px solid #505050;
            }
        """)
        
        self.init_ui()
        self.setup_shortcuts()
        self.load_saved_images()
        
    def init_ui(self):
        self.setWindowTitle("HeicViewer")
        self.setMinimumSize(800, 600)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.viewport().installEventFilter(self)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area.setWidget(self.image_label)
        self.setCentralWidget(self.scroll_area)
        create_menu(self)
        create_toolbar(self)
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
            self.open_heic_file(sys.argv[1])
    
    def setup_shortcuts(self):
        # Raccourcis de zoom
        zoom_in_shortcut = QShortcut(QKeySequence.StandardKey.ZoomIn, self)
        zoom_in_shortcut.activated.connect(self.zoom_in_shortcut)
        zoom_out_shortcut = QShortcut(QKeySequence.StandardKey.ZoomOut, self)
        zoom_out_shortcut.activated.connect(self.zoom_out_shortcut)
        zoom_in_plus_shortcut = QShortcut(QKeySequence("Ctrl++"), self)
        zoom_in_plus_shortcut.activated.connect(self.zoom_in_shortcut)
        zoom_out_minus_shortcut = QShortcut(QKeySequence("Ctrl+-"), self)
        zoom_out_minus_shortcut.activated.connect(self.zoom_out_shortcut)
        
        # Utiliser QShortcut à la place de QAction pour les touches directionnelles
        # afin d'éviter les conflits "Ambiguous shortcut overload"
        next_image_shortcut = QShortcut(QKeySequence("Right"), self)
        next_image_shortcut.activated.connect(self.next_image)
        next_image_shortcut.setContext(Qt.ShortcutContext.WindowShortcut)
        
        prev_image_shortcut = QShortcut(QKeySequence("Left"), self)
        prev_image_shortcut.activated.connect(self.prev_image)
        prev_image_shortcut.setContext(Qt.ShortcutContext.WindowShortcut)
        
        gallery_shortcut = QShortcut(QKeySequence("Ctrl+G"), self)
        gallery_shortcut.activated.connect(self.view_all_images)
    
    def zoom_in_shortcut(self):
        self.zoom_in()
        
    def zoom_out_shortcut(self):
        self.zoom_out()
    
    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Ouvrir une image HEIC",
            QStandardPaths.writableLocation(QStandardPaths.StandardLocation.PicturesLocation),
            "Images HEIC (*.heic *.HEIC);;Toutes les images (*.*);;Tous les fichiers (*)"
        )
        if file_path:
            self.open_heic_file(file_path)
    
    def set_quality(self, quality):
        self.jpeg_quality = quality
        if self.current_file_path:
            self.reload_current_image()
    
    def reload_current_image(self):
        if self.current_file_path:
            self.open_heic_file(self.current_file_path)
            
    def open_heic_file(self, file_path):
        try:
            self.current_file_path = file_path
            self.current_image, self.current_pixmap = load_image(file_path, self.jpeg_quality)
            self.current_scale = 1.0
            self.update_image_files_list(file_path)
            if self.is_fit_to_window:
                self.fit_to_window()
            else:
                self.show_original_size()
            img_size = self.current_image.size
            nav_info = f" - Image {self.current_index + 1}/{len(self.image_files)}" if self.image_files else ""
            self.status_bar.showMessage(f"{os.path.basename(file_path)} - {img_size[0]}x{img_size[1]} pixels{nav_info}")
            self.setWindowTitle(f"HeicViewer - {os.path.basename(file_path)}")
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Erreur lors de l'ouverture",
                f"Impossible d'ouvrir {file_path}:\n{str(e)}"
            )
    
    def update_image_files_list(self, current_file_path):
        directory = os.path.dirname(current_file_path)
        self.image_files = []
        for filename in sorted(os.listdir(directory)):
            if filename.lower().endswith(('.heic', '.heif')):
                full_path = os.path.join(directory, filename)
                self.image_files.append(full_path)
        try:
            self.current_index = self.image_files.index(current_file_path)
        except ValueError:
            self.current_index = -1
            
    def set_search_results(self, results):
        if results:
            self.search_results = results
            self.status_bar.showMessage(f"{len(results)} images HEIC trouvées - Utilisez 'Voir tout' pour les afficher")
            self.data_manager.add_search_result(results)

    def load_saved_images(self):
        """Charge les images sauvegardées au démarrage de l'application"""
        saved_images = self.data_manager.load_images()
        if saved_images:
            self.search_results = saved_images
            self.status_bar.showMessage(f"{len(saved_images)} images HEIC chargées depuis la session précédente")

    def view_all_images(self):
        if self.search_results and (not self.image_files or self.using_search_results):
            self.using_search_results = True
            images_to_display = self.search_results
            current_idx = 0
            if self.current_file_path and self.current_file_path in self.search_results:
                current_idx = self.search_results.index(self.current_file_path)
                
            dialog = ImageGalleryDialog(self, images_to_display, current_idx)
            result = dialog.exec()
            
            if result == QDialog.DialogCode.Accepted and dialog.selected_image_path:
                self.is_fit_to_window = True
                self.open_heic_file(dialog.selected_image_path)
                self.fit_to_window()
                self.using_search_results = True
                
        elif self.image_files:
            self.using_search_results = False
            dialog = ImageGalleryDialog(self, self.image_files, self.current_index)
            result = dialog.exec()
            
            if result == QDialog.DialogCode.Accepted and dialog.selected_image_path:
                self.is_fit_to_window = True
                self.open_heic_file(dialog.selected_image_path)
                self.fit_to_window()
        else:
            QMessageBox.information(self, "Information", "Aucune image HEIC disponible.")
    
    def next_image(self):
        if self.using_search_results and self.search_results:
            if self.current_file_path in self.search_results:
                current_idx = self.search_results.index(self.current_file_path)
                next_idx = (current_idx + 1) % len(self.search_results)
                self.open_heic_file(self.search_results[next_idx])
                return
        if self.image_files and self.current_index != -1:
            self.using_search_results = False
            self.current_index = (self.current_index + 1) % len(self.image_files)
            self.open_heic_file(self.image_files[self.current_index])
    
    def prev_image(self):
        if self.using_search_results and self.search_results:
            if self.current_file_path in self.search_results:
                current_idx = self.search_results.index(self.current_file_path)
                prev_idx = (current_idx - 1) % len(self.search_results)
                self.open_heic_file(self.search_results[prev_idx])
                return
        if self.image_files and self.current_index != -1:
            self.using_search_results = False
            self.current_index = (self.current_index - 1) % len(self.image_files)
            self.open_heic_file(self.image_files[self.current_index])
    
    def show_heic_finder(self):
        show_finder_dialog(self)
    
    def display_pixmap(self, pixmap):
        if pixmap:
            self.image_label.setPixmap(pixmap)
            
    def zoom_in(self, pos=None):
        if self.current_pixmap:
            self.is_fit_to_window = False
            scroll_pos_before = self.scroll_area.horizontalScrollBar().value(), self.scroll_area.verticalScrollBar().value()
            rel_pos = get_relative_position(pos, self.image_label, self.scroll_area) if pos else None
            self.current_scale *= self.zoom_factor
            width = int(self.current_pixmap.width() * self.current_scale)
            height = int(self.current_pixmap.height() * self.current_scale)
            scaled_pixmap = self.current_pixmap.scaled(
                width, height, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
            self.status_bar.showMessage(f"Zoom: {int(self.current_scale * 100)}%")
            if rel_pos:
                adjust_scroll_position(rel_pos, self.scroll_area, self.image_label)
    
    def zoom_out(self, pos=None):
        if self.current_pixmap:
            self.is_fit_to_window = False
            scroll_pos_before = self.scroll_area.horizontalScrollBar().value(), self.scroll_area.verticalScrollBar().value()
            rel_pos = get_relative_position(pos, self.image_label, self.scroll_area) if pos else None
            self.current_scale /= self.zoom_factor
            if self.current_scale < 0.1:
                self.current_scale = 0.1
            width = int(self.current_pixmap.width() * self.current_scale)
            height = int(self.current_pixmap.height() * self.current_scale)
            scaled_pixmap = self.current_pixmap.scaled(
                width, height, 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
            self.status_bar.showMessage(f"Zoom: {int(self.current_scale * 100)}%")
            if rel_pos:
                adjust_scroll_position(rel_pos, self.scroll_area, self.image_label)
    
    def fit_to_window(self):
        if self.current_pixmap:
            self.is_fit_to_window = True
            scroll_area_size = self.scroll_area.viewport().size()
            original_size = self.current_pixmap.size()
            scale_w = scroll_area_size.width() / original_size.width()
            scale_h = scroll_area_size.height() / original_size.height()
            self.current_scale = min(scale_w, scale_h)
            if self.current_scale > 2.0:
                self.current_scale = 2.0
            target_width = int(original_size.width() * self.current_scale)
            target_height = int(original_size.height() * self.current_scale)
            scaled_pixmap = self.current_pixmap.scaled(
                target_width, target_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.display_pixmap(scaled_pixmap)
            self.status_bar.showMessage(f"Zoom: {int(self.current_scale * 100)}% (ajusté à la fenêtre)")
    
    def show_original_size(self):
        if self.current_pixmap:
            self.is_fit_to_window = False
            self.current_scale = 1.0
            self.display_pixmap(self.current_pixmap)
            self.status_bar.showMessage("Zoom: 100% (taille originale)")
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.current_pixmap and self.is_fit_to_window:
            self.fit_to_window()
    
    def get_center_position(self):
        viewport = self.scroll_area.viewport()
        center_x = viewport.width() // 2
        center_y = viewport.height() // 2
        center_point = QPoint(center_x, center_y)
        
        return center_point
    
    def eventFilter(self, obj, event):
        if (obj is self.scroll_area.viewport() and 
            event.type() == event.Type.Wheel and 
            event.modifiers() & Qt.KeyboardModifier.ControlModifier and
            self.current_pixmap):
            delta = event.angleDelta().y()
            mouse_pos = event.position().toPoint()
            
            if delta > 0:
                self.zoom_in(mouse_pos)
            elif delta < 0:
                self.zoom_out(mouse_pos)
            return True
        return super().eventFilter(obj, event)
    
    def wheelEvent(self, event):
        super().wheelEvent(event)
    
    def show_about_dialog(self):
        show_about_dialog(self)
        
    def show_association_dialog(self):
        show_association_dialog(self)
    
    def create_file_association(self):
        create_file_association(self)
