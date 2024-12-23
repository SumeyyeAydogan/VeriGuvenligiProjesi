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
        """Görüntüye threshold uygula"""
        img_array = np.array(self.original_image)
        threshold = 128
        img_array = ((img_array > threshold) * 255).astype(np.uint8)
        self.dithered_image = Image.fromarray(img_array)
        return self.dithered_image

    def generate_shares(self):
        """(3,3) şeması için 3 pay oluştur"""
        if self.dithered_image is None:
            self.apply_dithering()

        # RGBA formatında payları oluştur (4 kanal: R,G,B,A)
        share1 = np.zeros((self.height*2, self.width*2, 4), dtype=np.uint8)
        share2 = np.zeros((self.height*2, self.width*2, 4), dtype=np.uint8)
        share3 = np.zeros((self.height*2, self.width*2, 4), dtype=np.uint8)

        binary_image = np.array(self.dithered_image) // 255

        # Temel desen matrisleri - siyah ve transparent için
        black_subpixels = [
            [[1,1,0,0], [0,0,1,1], [1,1,0,0]],  # Siyah piksel için desen 1
            [[0,0,1,1], [1,1,0,0], [0,0,1,1]]   # Siyah piksel için desen 2
        ]
        
        white_subpixels = [
            [[1,0,0,1], [0,1,1,0], [1,0,0,1]],  # Beyaz (transparent) piksel için desen 1
            [[0,1,1,0], [1,0,0,1], [0,1,1,0]]   # Beyaz (transparent) piksel için desen 2
        ]

        for y in range(self.height):
            for x in range(self.width):
                y2, x2 = y*2, x*2
                pattern_idx = random.randint(0, 1)
                
                if binary_image[y, x] == 1:  # Beyaz piksel (transparent olacak)
                    patterns = white_subpixels[pattern_idx]
                else:  # Siyah piksel
                    patterns = black_subpixels[pattern_idx]
                
                # Her pay için 2x2 alt pikselleri ayarla
                for i in range(2):
                    for j in range(2):
                        # Siyah nokta için [0,0,0,255], transparent için [0,0,0,0]
                        alpha_value = 255 if patterns[0][i*2+j] else 0
                        share1[y2+i,x2+j] = [0,0,0,alpha_value]
                        
                        alpha_value = 255 if patterns[1][i*2+j] else 0
                        share2[y2+i,x2+j] = [0,0,0,alpha_value]
                        
                        alpha_value = 255 if patterns[2][i*2+j] else 0
                        share3[y2+i,x2+j] = [0,0,0,alpha_value]

        self.shares = [
            Image.fromarray(share1, 'RGBA'),
            Image.fromarray(share2, 'RGBA'),
            Image.fromarray(share3, 'RGBA')
        ]
        return self.shares

    def create_pattern(self, pattern):
        """2x2 desenini RGBA formatına dönüştür"""
        rgba_pattern = np.zeros((2, 2, 4), dtype=np.uint8)
        for i in range(2):
            for j in range(2):
                if pattern[i][j] == 1:
                    # Siyah nokta: RGB(0,0,0) ve alpha=255
                    rgba_pattern[i,j] = [0, 0, 0, 255]
                else:
                    # Transparent: RGB(0,0,0) ve alpha=0
                    rgba_pattern[i,j] = [0, 0, 0, 0]
        return rgba_pattern

    def combine_shares(self):
        """Payları birleştirerek orijinal görüntüyü elde et"""
        if not self.shares:
            raise ValueError("Önce paylar oluşturulmalı!")

        # Payları numpy array'e dönüştür (sadece alpha kanalını kullan)
        share_arrays = [np.array(share)[:,:,3] == 255 for share in self.shares]
        
        # Mantıksal AND işlemi ile payları birleştir (fiziksel üst üste koyma işlemini simüle et)
        combined = share_arrays[0]
        for share in share_arrays[1:]:
            combined = np.logical_and(combined, share)
        
        # RGBA formatında sonuç oluştur
        result = np.zeros((combined.shape[0], combined.shape[1], 4), dtype=np.uint8)
        # Siyah noktalar için alpha=255, diğerleri için alpha=0
        result[combined] = [0, 0, 0, 255]  # Siyah noktalar
        result[~combined] = [255, 255, 255, 255]   # Beyaz alanlar
        
        return Image.fromarray(result, 'RGBA')