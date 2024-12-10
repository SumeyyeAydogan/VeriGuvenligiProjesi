"""
Görüntü işleme yardımcı fonksiyonları
"""

import os
from PIL import Image
import numpy as np

def save_image(image, path, filename):
    """
    Görüntüyü belirtilen yola kaydet
    
    Args:
        image: PIL.Image nesnesi
        path: Kaydedilecek dizin yolu
        filename: Dosya adı
    """
    if not os.path.exists(path):
        os.makedirs(path)
    full_path = os.path.join(path, filename)
    image.save(full_path)

def resize_image(image, max_size=800):
    """
    Görüntüyü en büyük boyutu max_size olacak şekilde yeniden boyutlandır
    
    Args:
        image: PIL.Image nesnesi
        max_size: İzin verilen maksimum boyut
    Returns:
        PIL.Image: Yeniden boyutlandırılmış görüntü
    """
    if max(image.size) <= max_size:
        return image
    
    ratio = max_size / max(image.size)
    new_size = tuple(int(dim * ratio) for dim in image.size)
    return image.resize(new_size, Image.Resampling.LANCZOS)

def convert_to_grayscale(image):
    """
    Renkli görüntüyü gri seviyeye dönüştür
    
    Args:
        image: PIL.Image nesnesi
    Returns:
        PIL.Image: Gri seviye görüntü
    """
    return image.convert('L') 