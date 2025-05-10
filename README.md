# HeicViewer

HeicViewer est une visionneuse d'images HEIC/HEIF open source créée avec Python et PyQt6, conçue pour offrir une expérience utilisateur fluide avec des fonctionnalités avancées.

## Fonctionnalités

- **Support complet des formats HEIC/HEIF** - Visualisation haute qualité des images HEIC/HEIF
- **Interface sombre moderne** - Design épuré et confortable pour une utilisation prolongée
- **Navigation intuitive** - Navigation facile entre les images d'un même dossier
- **Zoom intelligent** - Zoom centré sur la position du curseur
- **Recherche système** - Recherche de fichiers HEIC sur tout le système
- **Galerie d'aperçu** - Affichage miniature de toutes les images disponibles
- **Association de fichiers** - Association automatique des fichiers HEIC avec l'application
- **Haute qualité** - Rendu optimisé pour préserver la qualité des images
- **Multi-plateforme** - Fonctionne sur Windows, macOS et Linux

## Installation

### Prérequis

- Python 3.9 ou supérieur
- Pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
# Cloner le dépôt
git clone https://github.com/votre-username/HeicViewer.git
cd HeicViewer-app

# Installer les dépendances
pip install -r requirements.txt
```

### Exécution

```bash
python main.py
```

## Utilisation

### Ouverture d'images

- **Directement depuis l'explorateur** - Associez les fichiers HEIC avec HeicViewer (menu Aide > Associer les fichiers)
- **Via l'application** - Utilisez Fichier > Ouvrir ou appuyez sur Ctrl+O

### Navigation

- Utilisez les flèches gauche/droite pour naviguer entre les images
- Appuyez sur Ctrl+G pour afficher la galerie d'images

### Zoom et affichage

- Ctrl + Molette de souris pour zoomer/dézoomer
- Double-clic pour basculer entre l'ajustement à la fenêtre et la taille réelle
- Ctrl+0 pour ajuster à la fenêtre, Ctrl+1 pour la taille réelle

### Recherche de fichiers HEIC

1. Ouvrez l'outil de recherche via Fichier > Rechercher (ou Ctrl+F)
2. Sélectionnez l'emplacement de recherche
3. Activez/désactivez la recherche récursive selon vos besoins
4. Lancez la recherche

## Options de qualité

L'application propose trois niveaux de qualité pour le rendu des images:

- **Haute qualité** (par défaut): 100% de la qualité d'image
- **Qualité moyenne**: 80% de la qualité d'image
- **Basse qualité**: 60% de la qualité d'image



