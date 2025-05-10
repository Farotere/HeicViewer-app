#!/usr/bin/env python3
import sys
import os

# Ajouter le répertoire parent au chemin de recherche Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from src.ui.main_window import HeicViewer
from src.ui.theme import apply_theme

def main():
    app = QApplication(sys.argv)
    
    # Appliquer le thème premium
    apply_theme(app)
    
    viewer = HeicViewer()
    viewer.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
