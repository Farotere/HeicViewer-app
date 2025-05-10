"""
Module pour centraliser le thème sombre de l'application
"""

def get_dark_theme_stylesheet():
    """Retourne la feuille de style pour le thème sombre global"""
    return """
        /* Styles de base */
        QWidget {
            background-color: #232323;
            color: #E0E0E0;
        }
        
        /* Fenêtre principale */
        QMainWindow {
            background-color: #232323;
        }
        
        /* Labels */
        QLabel {
            color: #E0E0E0;
            background-color: transparent;
        }
        
        /* Boutons */
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
        
        /* Cases à cocher avec indication plus visible */
        QCheckBox {
            color: #E0E0E0;
            background-color: transparent;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            background-color: #AAAAAA;
            border: 1px solid #606060;
        }
        QCheckBox::indicator:unchecked {
            background-color: #555555;
        }
        QCheckBox::indicator:checked {
            background-color: #4080C0;
            border: 1px solid #6090D0;
            image: url(data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24"><path fill="white" d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/></svg>);
        }
        QCheckBox::indicator:hover {
            border: 1px solid #80A0E0;
        }
        
        /* Barres de défilement */
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
        
        /* Menu et barre d'outils */
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
        
        /* Barre de statut */
        QStatusBar {
            background-color: #303030;
            color: #E0E0E0;
            border-top: 1px solid #404040;
        }
        
        /* Listes et arbres */
        QTreeWidget, QListWidget, QTableWidget {
            background-color: #303030;
            color: #E0E0E0;
            border: 1px solid #404040;
            alternate-background-color: #353535;
        }
        QTreeWidget::item:selected, QListWidget::item:selected {
            background-color: #404050;
            color: #FFFFFF;
        }
        QHeaderView::section {
            background-color: #404040;
            color: #E0E0E0;
            border: 1px solid #505050;
        }
        
        /* Entrées texte et combos */
        QLineEdit, QComboBox, QSpinBox {
            background-color: #353535;
            color: #E0E0E0;
            border: 1px solid #505050;
            border-radius: 3px;
            padding: 3px;
        }
        QComboBox::drop-down {
            background-color: #404040;
        }
        QComboBox QAbstractItemView {
            background-color: #353535;
            color: #E0E0E0;
            border: 1px solid #505050;
            selection-background-color: #404050;
        }
        
        /* Progress bar */
        QProgressBar {
            border: 1px solid #505050;
            background-color: #353535;
            text-align: center;
            color: #E0E0E0;
            border-radius: 3px;
        }
        QProgressBar::chunk {
            background-color: #405060;
        }
        
        /* Tooltips et boites de dialogue */
        QToolTip, QMessageBox {
            background-color: #404040;
            color: #E0E0E0;
            border: 1px solid #505050;
        }
        QDialog {
            background-color: #232323;
        }
        
        /* Frames */
        QFrame {
            background-color: #333333;
            border: 1px solid #404040;
        }
    """

def apply_dark_theme_to_widget(widget):
    """Applique le thème sombre au widget spécifié"""
    widget.setStyleSheet(get_dark_theme_stylesheet())
