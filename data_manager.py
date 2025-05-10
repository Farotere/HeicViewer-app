import os
import json
import time
from PyQt6.QtCore import QStandardPaths

class HeicDataManager:
    """Gestionnaire pour stocker et récupérer les chemins d'images HEIC"""
    
    def __init__(self):
        # Dossier de données de l'application
        app_data_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
        self.app_data_dir = os.path.join(app_data_path, "HeicViewer")
        self.images_file = os.path.join(self.app_data_dir, "saved_images.json")
        self.recent_searches_file = os.path.join(self.app_data_dir, "recent_searches.json")
        
        # Créer le dossier s'il n'existe pas
        os.makedirs(self.app_data_dir, exist_ok=True)
    
    def save_images(self, image_paths):
        """Sauvegarde la liste des chemins d'images"""
        # Filtrer les chemins qui n'existent plus
        valid_paths = [path for path in image_paths if os.path.exists(path)]
        
        # Structure des données avec timestamp
        data = {
            "timestamp": time.time(),
            "images": valid_paths
        }
        
        try:
            with open(self.images_file, 'w') as f:
                json.dump(data, f)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des images: {e}")
            return False
    
    def load_images(self):
        """Charge la liste des chemins d'images"""
        if not os.path.exists(self.images_file):
            return []
            
        try:
            with open(self.images_file, 'r') as f:
                data = json.load(f)
                # Vérifier que chaque chemin existe encore
                valid_images = [path for path in data.get("images", []) if os.path.exists(path)]
                return valid_images
        except Exception as e:
            print(f"Erreur lors du chargement des images: {e}")
            return []
    
    def add_search_result(self, image_paths):
        """Ajoute des résultats de recherche à la liste des images sauvegardées"""
        # Combiner avec les images existantes
        existing_images = self.load_images()
        # Utiliser un ensemble pour éviter les doublons
        combined_images = list(set(existing_images + image_paths))
        return self.save_images(combined_images)
    
    def save_recent_search(self, search_path):
        """Sauvegarde un chemin de recherche récent"""
        try:
            if os.path.exists(self.recent_searches_file):
                with open(self.recent_searches_file, 'r') as f:
                    searches = json.load(f)
            else:
                searches = []
                
            # Ajouter le nouveau chemin en tête de liste s'il n'y est pas déjà
            if search_path in searches:
                searches.remove(search_path)
            searches.insert(0, search_path)
            
            # Limiter à 10 chemins récents
            searches = searches[:10]
            
            with open(self.recent_searches_file, 'w') as f:
                json.dump(searches, f)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des recherches récentes: {e}")
            return False
    
    def get_recent_searches(self):
        """Récupère les chemins de recherche récents"""
        if not os.path.exists(self.recent_searches_file):
            return []
            
        try:
            with open(self.recent_searches_file, 'r') as f:
                searches = json.load(f)
                # Vérifier que chaque chemin existe encore
                return [path for path in searches if os.path.exists(os.path.dirname(path))]
        except Exception as e:
            print(f"Erreur lors du chargement des recherches récentes: {e}")
            return []
