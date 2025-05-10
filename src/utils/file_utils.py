import platform
import os
import subprocess
import sys
from PyQt6.QtWidgets import QMessageBox

def show_about_dialog(parent):
    QMessageBox.about(
        parent,
        "À propos de HeicViewer",
        "HeicViewer\n\n"
        "Une visionneuse HEIC open source créée par Farotere\n"
        "Version 1.0.0\n\n"
        "Utilise Python, PyQt6, Pillow et pillow_heif\n"
        "Licence : MIT"
    )

def create_file_association(parent):
    system = platform.system()
    success = False
    message = ""
    
    try:
        if system == "Windows":
            success, message = create_windows_association()
        elif system == "Linux":
            success, message = create_linux_association()
        elif system == "Darwin":
            success, message = create_macos_association()
            
        if success:
            QMessageBox.information(parent, "Association créée", 
                                   f"Les fichiers .heic ont été associés avec success à HeicViewer.\n{message}")
        else:
            QMessageBox.warning(parent, "Échec de l'association", 
                               f"Impossible de créer l'association automatiquement.\n{message}")
    except Exception as e:
        QMessageBox.critical(parent, "Erreur", f"Une erreur est survenue: {str(e)}")
        
def create_windows_association():
    try:
        import winreg
        python_exe = sys.executable
        script_path = os.path.abspath(sys.argv[0])
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\.heic") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "HeicViewer.heicfile")
            
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\HeicViewer.heicfile") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, "Fichier HEIC")
            
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Classes\HeicViewer.heicfile\shell\open\command") as key:
            winreg.SetValue(key, "", winreg.REG_SZ, f'"{python_exe}" "{script_path}" "%1"')
            
        return True, "Association créée dans le registre Windows."
    except Exception as e:
        return False, f"Erreur lors de la création des clés de registre: {str(e)}"
        
def create_linux_association():
    try:
        app_path = os.path.abspath(sys.argv[0])
        desktop_dir = os.path.expanduser("~/.local/share/applications")
        os.makedirs(desktop_dir, exist_ok=True)
        desktop_file = os.path.join(desktop_dir, "heicviewer.desktop")
        with open(desktop_file, "w") as f:
            f.write(f"""[Desktop Entry]
Type=Application
Name=HeicViewer
Comment=Visionneuse d'images HEIC
Exec=python "{app_path}" %f
MimeType=image/heic;image/heif;
Terminal=false
Categories=Graphics;Viewer;
""")
        os.chmod(desktop_file, 0o755)
        subprocess.run(["xdg-mime", "default", "heicviewer.desktop", "image/heic"], check=True)
        subprocess.run(["xdg-mime", "default", "heicviewer.desktop", "image/heif"], check=True)
        subprocess.run(["update-desktop-database", desktop_dir], check=True, stderr=subprocess.DEVNULL)
        
        return True, f"Fichier d'association créé dans {desktop_file}"
    except Exception as e:
        return False, f"Erreur lors de la création de l'association: {str(e)}"
        
def create_macos_association():
    return False, "Sur macOS, l'association automatique n'est pas possible. Veuillez suivre les instructions manuelles."

def show_association_dialog(parent):
    system = platform.system()
    
    if system == "Windows":
        instructions = (
            "Pour associer les fichiers .heic à HeicViewer sur Windows :\n\n"
            "1. Cliquez-droit sur un fichier .heic\n"
            "2. Sélectionnez 'Ouvrir avec' > 'Choisir une autre application'\n"
            "3. Cliquez sur 'Plus d'applications' puis 'Rechercher une autre application sur ce PC'\n"
            "4. Naviguez jusqu'à l'exécutable Python et sélectionnez-le\n"
            "5. Ajoutez le chemin complet vers ce script comme argument\n"
            "6. Cochez la case 'Toujours utiliser cette application'\n"
            "7. Cliquez sur 'OK'"
        )
    elif system == "Darwin":
        instructions = (
            "Pour associer les fichiers .heic à HeicViewer sur macOS :\n\n"
            "1. Cliquez-droit sur un fichier .heic\n"
            "2. Sélectionnez 'Ouvrir avec' > 'Autre...'\n"
            "3. Naviguez jusqu'à ce script ou créez un .app avec py2app\n"
            "4. Cochez 'Toujours ouvrir avec'\n"
            "5. Cliquez sur 'Ouvrir'"
        )
    else:
        instructions = (
            "Pour associer les fichiers .heic à HeicViewer sur Linux :\n\n"
            "1. Créez un fichier .desktop dans ~/.local/share/applications/\n"
            "2. Ajoutez les entrées comme :\n"
            "   [Desktop Entry]\n"
            "   Type=Application\n"
            "   Name=HeicViewer\n"
            "   Exec=python /chemin/vers/heic_viewer.py %f\n"
            "   MimeType=image/heic;\n"
            "   Terminal=false\n\n"
            "3. Utilisez 'xdg-mime default heicviewer.desktop image/heic'"
        )
        
    QMessageBox.information(parent, "Associer les fichiers .heic", instructions)
