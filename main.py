#!/usr/bin/env python3
import sys
from PyQt6.QtWidgets import QApplication
from heic_viewer import HeicViewer

def main():
    app = QApplication(sys.argv)
    viewer = HeicViewer()
    viewer.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
