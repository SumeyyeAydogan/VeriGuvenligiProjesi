import numpy as np
from PIL import Image
import random
from ..image_processing.dithering import FloydSteinbergDithering

class VisualCryptography:
    def __init__(self, image_path):
        """
        (3,3) görsel şifreleme için sınıf başlatıcı
        Args:
            image_path: Giriş görüntüsünün yolu
        """
        self.original_image = Image.open(image_path).convert('L')
        self.width, self.height = self.original_image.size
        self.dithered_image = None
        self.shares = []

    def apply_dithering(self):
        """Görüntüye Floyd-Steinberg dithering uygula"""
        dithering = FloydSteinbergDithering()
        self.dithered_image = dithering.apply(self.original_image)
        return self.dithered_image

    def generate_shares(self):
        """(3,3) şeması için 3 pay oluştur"""
        if self.dithered_image is None:
            self.apply_dithering()

        # Her pay için 2x boyutlu boş görüntüler oluştur
        share1 = np.zeros((self.height*2, self.width*2), dtype=np.uint8)
        share2 = np.zeros((self.height*2, self.width*2), dtype=np.uint8)
        share3 = np.zeros((self.height*2, self.width*2), dtype=np.uint8)

        binary_image = np.array(self.dithered_image) // 255

        for y in range(self.height):
            for x in range(self.width):
                if binary_image[y, x] == 1:  # Beyaz piksel
                    # Beyaz piksel için rastgele bir desen seç
                    if random.random() < 0.5:
                        share1[y*2:y*2+2, x*2:x*2+2] = np.array([[255, 0], [0, 255]])
                        share2[y*2:y*2+2, x*2:x*2+2] = np.array([[0, 255], [255, 0]])
                        share3[y*2:y*2+2, x*2:x*2+2] = np.array([[255, 0], [0, 255]])
                    else:
                        share1[y*2:y*2+2, x*2:x*2+2] = np.array([[0, 255], [255, 0]])
                        share2[y*2:y*2+2, x*2:x*2+2] = np.array([[255, 0], [0, 255]])
                        share3[y*2:y*2+2, x*2:x*2+2] = np.array([[0, 255], [255, 0]])
                else:  # Siyah piksel
                    # Siyah piksel için rastgele bir desen seç
                    pattern = random.randint(0, 3)
                    if pattern == 0:
                        share1[y*2:y*2+2, x*2:x*2+2] = np.array([[255, 255], [0, 0]])
                        share2[y*2:y*2+2, x*2:x*2+2] = np.array([[0, 0], [255, 255]])
                        share3[y*2:y*2+2, x*2:x*2+2] = np.array([[255, 255], [0, 0]])
                    elif pattern == 1:
                        share1[y*2:y*2+2, x*2:x*2+2] = np.array([[0, 0], [255, 255]])
                        share2[y*2:y*2+2, x*2:x*2+2] = np.array([[255, 255], [0, 0]])
                        share3[y*2:y*2+2, x*2:x*2+2] = np.array([[0, 0], [255, 255]])
                    elif pattern == 2:
                        share1[y*2:y*2+2, x*2:x*2+2] = np.array([[255, 0], [255, 0]])
                        share2[y*2:y*2+2, x*2:x*2+2] = np.array([[0, 255], [0, 255]])
                        share3[y*2:y*2+2, x*2:x*2+2] = np.array([[255, 0], [255, 0]])
                    else:
                        share1[y*2:y*2+2, x*2:x*2+2] = np.array([[0, 255], [0, 255]])
                        share2[y*2:y*2+2, x*2:x*2+2] = np.array([[255, 0], [255, 0]])
                        share3[y*2:y*2+2, x*2:x*2+2] = np.array([[0, 255], [0, 255]])

        self.shares = [
            Image.fromarray(share1),
            Image.fromarray(share2),
            Image.fromarray(share3)
        ]
        return self.shares

    def combine_shares(self):
        """Payları birleştirerek orijinal görüntüyü elde et"""
        if not self.shares:
            raise ValueError("Önce paylar oluşturulmalı!")

        # Payları numpy array'e dönüştür
        share_arrays = [np.array(share) for share in self.shares]
        
        # Payları mantıksal VEYA (OR) işlemi ile birleştir
        combined = share_arrays[0]
        for share in share_arrays[1:]:
            combined = np.bitwise_or(combined, share)
        
        return Image.fromarray(combined)