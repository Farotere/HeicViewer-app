import io
import os
import sys  # Ajout de cet import
from PyQt6.QtCore import QStandardPaths
from PyQt6.QtGui import QPixmap, QImage
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()

def load_image(file_path, quality=100):
    pil_image = Image.open(file_path)
    pixmap = convert_pil_to_pixmap(pil_image, quality)
    
    return pil_image, pixmap

def convert_pil_to_pixmap(pil_image, quality=100):
    try:
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")
        
        buffer = io.BytesIO()
        
        # Sur Windows, utiliser PNG pour une meilleure qualité
        if sys.platform == "win32":
            pil_image.save(buffer, format="PNG")
        else:
            pil_image.save(buffer, format="JPEG", quality=quality, optimize=True, subsampling=0)
            
        buffer.seek(0)
        qimage = QImage.fromData(buffer.getvalue())
        return QPixmap.fromImage(qimage)
        
    except Exception as e:
        print(f"Erreur lors de la conversion de l'image: {e}")
        temp_path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.TempLocation), "temp_heic.jpg")
        
        # Utiliser PNG sur Windows pour une meilleure qualité
        if sys.platform == "win32":
            temp_path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.TempLocation), "temp_heic.png")
            pil_image.save(temp_path, "PNG")
        else:
            pil_image.save(temp_path, "JPEG", quality=quality, optimize=True, subsampling=0)
        
        pixmap = QPixmap(temp_path)
        try:
            os.remove(temp_path)
        except:
            pass
        
        return pixmap
