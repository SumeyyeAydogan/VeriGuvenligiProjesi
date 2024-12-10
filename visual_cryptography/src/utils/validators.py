"""
Doğrulama fonksiyonları
"""

import os
from PIL import Image

def validate_image_path(image_path):
    """
    Görüntü dosyasının geçerliliğini kontrol et
    
    Args:
        image_path: Kontrol edilecek dosya yolu
    Raises:
        FileNotFoundError: Dosya bulunamazsa
        ValueError: Geçersiz görüntü dosyası ise
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Görüntü dosyası bulunamadı: {image_path}")
    
    try:
        with Image.open(image_path) as img:
            img.verify()
    except Exception:
        raise ValueError(f"Geçersiz görüntü dosyası: {image_path}")

def validate_output_path(output_path):
    """
    Çıktı dizininin geçerliliğini kontrol et ve gerekirse oluştur
    
    Args:
        output_path: Kontrol edilecek dizin yolu
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    elif not os.path.isdir(output_path):
        raise NotADirectoryError(f"Belirtilen yol bir dizin değil: {output_path}")
