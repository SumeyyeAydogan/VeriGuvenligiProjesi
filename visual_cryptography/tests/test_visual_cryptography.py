import unittest
import numpy as np
from PIL import Image
import os
from src.cryptography.visual_cryptography import VisualCryptography

class TestVisualCryptography(unittest.TestCase):
    def setUp(self):
        """Test için gerekli dosya ve nesneleri hazırla"""
        # Test görüntüsü için dizin oluştur
        self.test_dir = "test_images"
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
            
        # Test için basit bir görüntü oluştur (4x4 gri seviye görüntü)
        self.test_image_path = os.path.join(self.test_dir, "test_image.png")
        test_image = Image.fromarray(np.array([
            [100, 150, 200, 50],
            [180, 120, 90, 220],
            [70, 140, 130, 110],
            [160, 30, 170, 80]
        ], dtype=np.uint8))
        test_image.save(self.test_image_path)
        
        # VisualCryptography nesnesini oluştur
        self.vc = VisualCryptography(self.test_image_path)

    def tearDown(self):
        """Test sonrası geçici dosyaları temizle"""
        if os.path.exists(self.test_dir):
            for file in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, file))
            os.rmdir(self.test_dir)

    def test_initialization(self):
        """Sınıf başlatma işleminin doğru çalıştığını kontrol et"""
        self.assertIsNotNone(self.vc.original_image)
        self.assertEqual(self.vc.width, 4)
        self.assertEqual(self.vc.height, 4)

    def test_dithering(self):
        """Dithering işleminin doğru çalıştığını kontrol et"""
        dithered = self.vc.apply_dithering()
        self.assertIsNotNone(dithered)
        
        # Dithering sonrası görüntünün binary olduğunu kontrol et
        dithered_array = np.array(dithered)
        unique_values = np.unique(dithered_array)
        self.assertTrue(all(val in [0, 255] for val in unique_values))

    def test_share_generation(self):
        """Pay oluşturma işleminin doğru çalıştığını kontrol et"""
        shares = self.vc.generate_shares()
        
        # 3 pay oluşturulduğunu kontrol et
        self.assertEqual(len(shares), 3)
        
        # Her payın boyutunun orijinal görüntünün 2 katı olduğunu kontrol et
        for share in shares:
            self.assertEqual(share.size, (self.vc.width * 2, self.vc.height * 2))
            
            # Payların binary olduğunu kontrol et
            share_array = np.array(share)
            unique_values = np.unique(share_array)
            self.assertTrue(all(val in [0, 255] for val in unique_values))

    def test_share_combination(self):
        """Payların birleştirilmesinin doğru çalıştığını kontrol et"""
        # Önce payları oluştur
        self.vc.generate_shares()
        
        # Payları birleştir
        combined = self.vc.combine_shares()
        self.assertIsNotNone(combined)
        
        # Birleştirilmiş görüntünün boyutunun doğru olduğunu kontrol et
        self.assertEqual(combined.size, (self.vc.width * 2, self.vc.height * 2))
        
        # Birleştirilmiş görüntünün binary olduğunu kontrol et
        combined_array = np.array(combined)
        unique_values = np.unique(combined_array)
        self.assertTrue(all(val in [0, 255] for val in unique_values))

    def test_share_independence(self):
        """Her payın bağımsız olduğunu kontrol et"""
        shares = self.vc.generate_shares()
        
        # Her payın diğerlerinden farklı olduğunu kontrol et
        for i in range(len(shares)):
            for j in range(i + 1, len(shares)):
                self.assertFalse(np.array_equal(
                    np.array(shares[i]),
                    np.array(shares[j])
                ))

    def test_invalid_share_combination(self):
        """Paylar oluşturulmadan birleştirme işleminin hata verdiğini kontrol et"""
        with self.assertRaises(ValueError):
            self.vc.combine_shares()

if __name__ == '__main__':
    unittest.main()
