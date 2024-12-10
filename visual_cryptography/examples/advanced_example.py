"""
Gelişmiş Visual Cryptography örneği
Bu örnek, birden fazla görüntü üzerinde işlem yapma, farklı parametreler kullanma
ve sonuçları karşılaştırma gibi gelişmiş özellikleri gösterir.
"""

import os
import sys

# Proje kök dizinini Python path'ine ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image
import numpy as np
from src.cryptography.visual_cryptography import VisualCryptography
from src.image_processing.dithering import FloydSteinbergDithering

def process_image(image_path, threshold=128):
    """Bir görüntüyü işle ve sonuçları döndür"""
    vc = VisualCryptography(image_path)
    
    # Dithering uygula
    dithered = vc.apply_dithering()
    
    # Payları oluştur
    shares = vc.generate_shares()
    
    # Payları birleştir
    combined = vc.combine_shares()
    
    return dithered, shares, combined

def compare_results(original, combined):
    """Orijinal ve birleştirilmiş görüntüleri karşılaştır"""
    # Görüntüleri aynı boyuta getir
    original_resized = original.resize(combined.size)
    
    # Görüntüleri array'e dönüştür
    orig_array = np.array(original_resized)
    comb_array = np.array(combined)
    
    # Piksel farklarının ortalamasını hesapla
    diff = np.mean(np.abs(orig_array - comb_array))
    return diff

def main():
    # Dizinleri tanımla
    input_dir = os.path.join('input', 'sample_images')
    output_dir = os.path.join('output')
    
    # Çıktı dizinlerini oluştur
    os.makedirs(os.path.join(output_dir, 'dithered'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'shares'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'combined'), exist_ok=True)
    
    # Tüm test görüntüleri üzerinde işlem yap
    for image_file in os.listdir(input_dir):
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"\nİşleniyor: {image_file}")
            
            image_path = os.path.join(input_dir, image_file)
            base_name = os.path.splitext(image_file)[0]
            
            try:
                # Görüntüyü işle
                dithered, shares, combined = process_image(image_path)
                
                # Sonuçları kaydet
                dithered.save(os.path.join(output_dir, 'dithered', f'dithered_{base_name}.png'))
                
                for i, share in enumerate(shares, 1):
                    share.save(os.path.join(output_dir, 'shares', f'share_{i}_{base_name}.png'))
                
                combined.save(os.path.join(output_dir, 'combined', f'combined_{base_name}.png'))
                
                # Sonuçları karşılaştır
                original = Image.open(image_path).convert('L')
                diff = compare_results(original, combined)
                print(f"Görüntü kalite farkı: {diff:.2f}")
                
            except Exception as e:
                print(f"Hata oluştu ({image_file}): {str(e)}")
                continue
            
            print(f"{image_file} işlemi tamamlandı.")

if __name__ == "__main__":
    main()
