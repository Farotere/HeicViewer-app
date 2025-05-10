"""
Module de thème pour HeicViewer Premium
Fournit un style cohérent et élégant à l'ensemble de l'application
"""
from PyQt6.QtGui import QColor, QPalette, QFont
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QSize

# Palette de couleurs sophistiquée
class PremiumColors:
    # Couleurs de base
    PRIMARY = "#1E88E5"         # Bleu primaire
    SECONDARY = "#26A69A"       # Turquoise pour accent secondaire
    BACKGROUND = "#FFFFFF"      # Fond clair
    DARK_BG = "#F5F5F7"         # Fond légèrement teinté
    TEXT = "#202124"            # Texte presque noir
    TEXT_SECONDARY = "#5F6368"  # Texte secondaire
    
    # Couleurs d'état
    SUCCESS = "#43A047"         # Vert succès
    ERROR = "#E53935"           # Rouge erreur
    WARNING = "#FFB300"         # Orange avertissement
    
    # Couleurs d'interface
    BORDER = "#E0E0E0"          # Bordures légères
    HOVER = "#E8F0FE"           # Survol
    SELECTION = "#BBDEFB"       # Sélection
    
    # Couleurs graduelles pour les éléments principaux
    PRIMARY_LIGHT = "#90CAF9"
    PRIMARY_DARK = "#1565C0"
    
    # Mode sombre (préparation)
    DARK_PRIMARY = "#2196F3"
    DARK_BACKGROUND = "#121212"
    DARK_SURFACE = "#1E1E1E"
    DARK_TEXT = "#FFFFFF"

# Configuration des dimensions et espacements
class Dimensions:
    PADDING_SMALL = 4
    PADDING = 8
    PADDING_LARGE = 16
    
    BORDER_RADIUS = 4
    BORDER_RADIUS_LARGE = 8
    
    BUTTON_HEIGHT = 32
    ICON_SIZE = 24
    THUMBNAIL_SIZE = 160

# Style principal
MAIN_STYLESHEET = f"""
    /* Style général de l'application */
    QMainWindow, QDialog {{
        background-color: {PremiumColors.BACKGROUND};
        color: {PremiumColors.TEXT};
    }}
    
    /* Barre de titre */
    QMainWindow::title {{
        background-color: {PremiumColors.PRIMARY};
        color: white;
        font-weight: bold;
    }}
    
    /* Boutons */
    QPushButton {{
        background-color: {PremiumColors.PRIMARY};
        color: white;
        border: none;
        border-radius: {Dimensions.BORDER_RADIUS}px;
        padding: {Dimensions.PADDING}px {Dimensions.PADDING_LARGE}px;
        font-weight: 500;
        min-height: {Dimensions.BUTTON_HEIGHT}px;
    }}
    
    QPushButton:hover {{
        background-color: {PremiumColors.PRIMARY_DARK};
    }}
    
    QPushButton:pressed {{
        background-color: {PremiumColors.PRIMARY_DARK};
        padding-top: {Dimensions.PADDING + 1}px;
    }}
    
    QPushButton:disabled {{
        background-color: {PremiumColors.BORDER};
        color: {PremiumColors.TEXT_SECONDARY};
    }}
    
    /* Bouton secondaire */
    QPushButton[secondary="true"] {{
        background-color: white;
        color: {PremiumColors.PRIMARY};
        border: 1px solid {PremiumColors.PRIMARY};
    }}
    
    QPushButton[secondary="true"]:hover {{
        background-color: {PremiumColors.HOVER};
    }}
    
    /* Bouton plat */
    QPushButton:flat {{
        background-color: transparent;
        color: {PremiumColors.PRIMARY};
        border: none;
    }}
    
    QPushButton:flat:hover {{
        background-color: {PremiumColors.HOVER};
    }}
    
    /* Case à cocher */
    QCheckBox {{
        spacing: 8px;
    }}
    
    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border: 2px solid {PremiumColors.TEXT_SECONDARY};
        border-radius: 3px;
    }}
    
    QCheckBox::indicator:checked {{
        background-color: {PremiumColors.PRIMARY};
        border-color: {PremiumColors.PRIMARY};
        image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="white"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>');
    }}
    
    QCheckBox::indicator:hover {{
        border-color: {PremiumColors.PRIMARY};
    }}
    
    /* MenuBar */
    QMenuBar {{
        background-color: {PremiumColors.DARK_BG};
        color: {PremiumColors.TEXT};
        border-bottom: 1px solid {PremiumColors.BORDER};
    }}
    
    QMenuBar::item {{
        background: transparent;
        padding: 6px 10px;
    }}
    
    QMenuBar::item:selected {{
        background-color: {PremiumColors.SELECTION};
        color: {PremiumColors.PRIMARY_DARK};
    }}
    
    QMenu {{
        background-color: white;
        border: 1px solid {PremiumColors.BORDER};
        border-radius: {Dimensions.BORDER_RADIUS}px;
        padding: 4px 0px;
    }}
    
    QMenu::item {{
        padding: 6px 24px 6px 12px;
        border-radius: 2px;
        margin: 2px 4px;
    }}
    
    QMenu::item:selected {{
        background-color: {PremiumColors.SELECTION};
        color: {PremiumColors.PRIMARY_DARK};
    }}
    
    /* ToolBar */
    QToolBar {{
        background-color: {PremiumColors.DARK_BG};
        border-bottom: 1px solid {PremiumColors.BORDER};
        spacing: 4px;
        padding: 2px;
    }}
    
    QToolBar QToolButton {{
        background-color: transparent;
        color: {PremiumColors.TEXT};
        border: none;
        border-radius: {Dimensions.BORDER_RADIUS}px;
        padding: 4px;
    }}
    
    QToolBar QToolButton:hover {{
        background-color: {PremiumColors.HOVER};
    }}
    
    QToolBar QToolButton:checked {{
        background-color: {PremiumColors.SELECTION};
        color: {PremiumColors.PRIMARY_DARK};
    }}
    
    /* Scroll area */
    QScrollArea {{
        border: none;
        background-color: transparent;
    }}
    
    /* ScrollBar */
    QScrollBar {{
        background-color: transparent;
        width: 10px;
        height: 10px;
    }}
    
    QScrollBar::handle {{
        background-color: {PremiumColors.TEXT_SECONDARY};
        border-radius: 4px;
        min-height: 32px;
    }}
    
    QScrollBar::handle:hover {{
        background-color: {PremiumColors.PRIMARY};
    }}
    
    QScrollBar::add-line, QScrollBar::sub-line {{
        height: 0px;
        width: 0px;
    }}
    
    QScrollBar::add-page, QScrollBar::sub-page {{
        background: none;
    }}
    
    /* StatusBar */
    QStatusBar {{
        background-color: {PremiumColors.DARK_BG};
        color: {PremiumColors.TEXT_SECONDARY};
        border-top: 1px solid {PremiumColors.BORDER};
        padding: 2px 8px;
    }}
    
    /* QLabel */
    QLabel {{
        color: {PremiumColors.TEXT};
    }}
    
    QLabel[heading="true"] {{
        font-weight: bold;
        font-size: 16px;
        color: {PremiumColors.PRIMARY_DARK};
    }}
    
    QLabel[subheading="true"] {{
        font-size: 14px;
        color: {PremiumColors.TEXT_SECONDARY};
    }}
    
    /* QLineEdit */
    QLineEdit {{
        padding: 8px;
        border: 1px solid {PremiumColors.BORDER};
        border-radius: {Dimensions.BORDER_RADIUS}px;
        selection-background-color: {PremiumColors.SELECTION};
    }}
    
    QLineEdit:focus {{
        border: 2px solid {PremiumColors.PRIMARY_LIGHT};
    }}
    
    /* QComboBox */
    QComboBox {{
        padding: 6px 12px;
        border: 1px solid {PremiumColors.BORDER};
        border-radius: {Dimensions.BORDER_RADIUS}px;
        min-height: {Dimensions.BUTTON_HEIGHT}px;
    }}
    
    QComboBox:hover {{
        border: 1px solid {PremiumColors.PRIMARY_LIGHT};
    }}
    
    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: right center;
        width: 24px;
        border: none;
    }}
    
    /* QProgressBar */
    QProgressBar {{
        border: none;
        text-align: center;
        color: white;
        background-color: {PremiumColors.BORDER};
        border-radius: 2px;
        height: 8px;
    }}
    
    QProgressBar::chunk {{
        background-color: {PremiumColors.PRIMARY};
        border-radius: 2px;
    }}
    
    /* QTreeWidget */
    QTreeWidget {{
        border: 1px solid {PremiumColors.BORDER};
        border-radius: {Dimensions.BORDER_RADIUS}px;
        background-color: white;
    }}
    
    QTreeWidget::item {{
        padding: 4px;
        border-radius: {Dimensions.BORDER_RADIUS}px;
        margin: 2px 4px;
    }}
    
    QTreeWidget::item:hover {{
        background-color: {PremiumColors.HOVER};
    }}
    
    QTreeWidget::item:selected {{
        background-color: {PremiumColors.SELECTION};
        color: {PremiumColors.PRIMARY_DARK};
    }}
    
    QTreeWidget QHeaderView::section {{
        background-color: {PremiumColors.DARK_BG};
        padding: 6px;
        border: none;
        border-right: 1px solid {PremiumColors.BORDER};
        font-weight: bold;
    }}
    
    /* Frames */
    QFrame[frameShape="4"] {{ /* StyledPanel */
        border: 1px solid {PremiumColors.BORDER};
        border-radius: {Dimensions.BORDER_RADIUS}px;
        background-color: white;
        padding: 4px;
    }}
"""

def apply_theme(app):
    """Applique le thème premium à l'application"""
    # Police de caractères
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Palette de couleurs
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(PremiumColors.BACKGROUND))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(PremiumColors.TEXT))
    palette.setColor(QPalette.ColorRole.Base, QColor(PremiumColors.BACKGROUND))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(PremiumColors.DARK_BG))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(PremiumColors.DARK_BG))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(PremiumColors.TEXT))
    palette.setColor(QPalette.ColorRole.Text, QColor(PremiumColors.TEXT))
    palette.setColor(QPalette.ColorRole.Button, QColor(PremiumColors.PRIMARY))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("white"))
    palette.setColor(QPalette.ColorRole.Link, QColor(PremiumColors.PRIMARY))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(PremiumColors.SELECTION))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(PremiumColors.PRIMARY_DARK))
    app.setPalette(palette)
    
    # Application de la feuille de style
    app.setStyleSheet(MAIN_STYLESHEET)

# Style spécifique pour les miniatures de la galerie
GALLERY_STYLE = f"""
.thumbnail-frame {{
    background-color: white;
    border: 1px solid {PremiumColors.BORDER};
    border-radius: {Dimensions.BORDER_RADIUS}px;
    padding: 4px;
}}

.thumbnail-frame:hover {{
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    border: 1px solid {PremiumColors.PRIMARY_LIGHT};
}}

.thumbnail-selected {{
    background-color: {PremiumColors.HOVER};
    border: 2px solid {PremiumColors.PRIMARY};
    border-radius: {Dimensions.BORDER_RADIUS}px;
}}

.number-label {{
    color: {PremiumColors.TEXT_SECONDARY};
    font-size: 11px;
    font-weight: bold;
}}

.number-selected {{
    color: {PremiumColors.PRIMARY};
    font-weight: bold;
    font-size: 12px;
}}

.image-name {{
    color: {PremiumColors.TEXT};
    font-size: 12px;
    text-align: center;
    margin-top: 2px;
}}
"""

# Constantes pour les icônes de l'interface (format SVG en base64)
ICONS = {
    "open": "M19 3H5c-1.11 0-2 .9-2 2v14c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14zm-8-2h2v-4h4v-2h-4V7h-2v4H7v2h4z",
    "search": "M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z",
    "prev": "M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z",
    "next": "M10.59 6L12 7.41 7.83 12 12 16.59 10.59 18l-6-6z", 
    "gallery": "M20 4v12H8V4h12m0-2H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-8.5 9.67l1.69 2.26 2.48-3.1L19 15H9zM2 6v14c0 1.1.9 2 2 2h14v-2H4V6H2z",
    "zoom_in": "M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z M12 10h-2v2H9v-2H7V9h2V7h1v2h2v1z",
    "zoom_out": "M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14zM7 9h5v1H7z",
    "fit": "M15 3l2.3 2.3-2.89 2.87 1.42 1.42L18.7 6.7 21 9V3zM3 9l2.3-2.3 2.87 2.89 1.42-1.42L6.7 5.3 9 3H3zm6 12l-2.3-2.3 2.89-2.87-1.42-1.42L5.3 17.3 3 15v6zm12-6l-2.3 2.3-2.87-2.89-1.42 1.42 2.89 2.87L15 21h6z",
    "original": "M21 3H3C2 3 1 4 1 5v14c0 1.1.9 2 2 2h18c1 0 2-1 2-2V5c0-1-1-2-2-2zM5 17l3.5-4.5 2.5 3.01L14.5 11l4.5 6H5z"
}

def get_svg_icon(icon_name):
    """Génère une icône SVG à partir des constantes"""
    if icon_name not in ICONS:
        return ""
    
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="{ICONS[icon_name]}"/></svg>'
