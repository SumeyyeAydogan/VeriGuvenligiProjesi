import unittest
import os
from src.utils.validators import validate_image_path
from PIL import Image

class TestUtils(unittest.TestCase):
    def setUp(self):
        """Test için geçici dosyalar oluştur"""
        self.valid_image_path = 'test_image.png'
        self.invalid_image_path = 'non_existent_image.png'
        self.invalid_file_path = 'invalid_file.txt'
        
        # Geçerli bir görüntü dosyası oluştur
        image = Image.new('RGB', (10, 10), color = 'white')
        image.save(self.valid_image_path)
        
        # Geçersiz bir dosya oluştur
        with open(self.invalid_file_path, 'w') as f:
            f.write("This is not an image file.")

    def tearDown(self):
        """Test sonrası geçici dosyaları sil"""
        if os.path.exists(self.valid_image_path):
            os.remove(self.valid_image_path)
        if os.path.exists(self.invalid_file_path):
            os.remove(self.invalid_file_path)

    def test_validate_image_path_valid(self):
        """Geçerli bir görüntü yolunun doğrulandığını kontrol et"""
        try:
            validate_image_path(self.valid_image_path)
        except Exception as e:
            self.fail(f"validate_image_path() raised {type(e).__name__} unexpectedly!")

    def test_validate_image_path_invalid(self):
        """Geçersiz bir görüntü yolunun hata verdiğini kontrol et"""
        with self.assertRaises(FileNotFoundError):
            validate_image_path(self.invalid_image_path)

    def test_validate_image_path_invalid_file(self):
        """Geçersiz bir dosya türünün hata verdiğini kontrol et"""
        with self.assertRaises(ValueError):
            validate_image_path(self.invalid_file_path)

if __name__ == '__main__':
    unittest.main()
