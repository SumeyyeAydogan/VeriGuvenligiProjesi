import unittest
import numpy as np
from PIL import Image
from src.image_processing.dithering import FloydSteinbergDithering

class TestDithering(unittest.TestCase):
    def setUp(self):
        """Test için gerekli nesneleri hazırla"""
        # Test için 4x4 gri seviye görüntü oluştur
        self.test_image = Image.fromarray(np.array([
            [100, 150, 200, 50],
            [180, 120, 90, 220],
            [70, 140, 130, 110],
            [160, 30, 170, 80]
        ], dtype=np.uint8))
        
        self.dithering = FloydSteinbergDithering()

    def test_dithering_output_size(self):
        """Dithering sonrası görüntü boyutunun değişmediğini kontrol et"""
        result = self.dithering.apply(self.test_image)
        self.assertEqual(result.size, self.test_image.size)

    def test_dithering_binary_output(self):
        """Dithering sonrası görüntünün sadece siyah ve beyaz piksellerden oluştuğunu kontrol et"""
        result = self.dithering.apply(self.test_image)
        result_array = np.array(result)
        unique_values = np.unique(result_array)
        self.assertTrue(all(val in [0, 255] for val in unique_values))

    def test_dithering_with_different_threshold(self):
        """Farklı eşik değerleriyle dithering'in çalıştığını kontrol et"""
        # Düşük eşik değeri (daha fazla beyaz piksel)
        result_low = self.dithering.apply(self.test_image, threshold=50)
        # Yüksek eşik değeri (daha fazla siyah piksel)
        result_high = self.dithering.apply(self.test_image, threshold=200)
        
        # Düşük eşik değerinde daha fazla beyaz piksel olmalı
        white_pixels_low = np.sum(np.array(result_low) == 255)
        white_pixels_high = np.sum(np.array(result_high) == 255)
        self.assertGreater(white_pixels_low, white_pixels_high)

    def test_dithering_with_empty_image(self):
        """Boş görüntü ile dithering'in hata vermeden çalıştığını kontrol et"""
        empty_image = Image.fromarray(np.zeros((1, 1), dtype=np.uint8))
        result = self.dithering.apply(empty_image)
        self.assertEqual(result.size, (1, 1))

    def test_error_diffusion(self):
        """Hata yayılımının doğru çalıştığını kontrol et"""
        # Tek bir gri piksel içeren test görüntüsü
        test_image = Image.fromarray(np.array([[128]], dtype=np.uint8))
        result = self.dithering.apply(test_image)
        
        # 128 değeri eşik değeri 128'e eşit olduğunda siyah olmalı
        self.assertEqual(np.array(result)[0, 0], 0)

if __name__ == '__main__':
    unittest.main()
