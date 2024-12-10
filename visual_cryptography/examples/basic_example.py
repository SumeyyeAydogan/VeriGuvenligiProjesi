"""
Temel Visual Cryptography örneği
Bu örnek, tek bir görüntü üzerinde (3,3) görsel şifreleme şemasının nasıl kullanılacağını gösterir.
"""

import os
import sys

# Proje kök dizinini Python path'ine ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cryptography.visual_cryptography import VisualCryptography

def main():
    # Giriş ve çıkış dizinlerini tanımla
    input_dir = os.path.join('input', 'sample_images')
    output_dir = os.path.join('output')
    
    # Test görüntüsünün yolu
    image_path = os.path.join(input_dir, 'test_image.png')
    
    try:
        # Visual Cryptography nesnesini oluştur
        vc = VisualCryptography(image_path)
        
        # Dithering uygula ve sonucu kaydet
        dithered = vc.apply_dithering()
        os.makedirs(os.path.join(output_dir, 'dithered'), exist_ok=True)
        dithered.save(os.path.join(output_dir, 'dithered', 'dithered_image.png'))
        
        # Payları oluştur ve kaydet
        shares = vc.generate_shares()
        os.makedirs(os.path.join(output_dir, 'shares'), exist_ok=True)
        for i, share in enumerate(shares, 1):
            share.save(os.path.join(output_dir, 'shares', f'share_{i}.png'))
        
        # Payları birleştir ve sonucu kaydet
        combined = vc.combine_shares()
        os.makedirs(os.path.join(output_dir, 'combined'), exist_ok=True)
        combined.save(os.path.join(output_dir, 'combined', 'combined_image.png'))
        
        print("İşlem başarıyla tamamlandı!")
        print(f"Sonuçlar {output_dir} dizininde bulunabilir.")
        
    except Exception as e:
        print(f"Hata oluştu: {str(e)}")

if __name__ == "__main__":
    main()
