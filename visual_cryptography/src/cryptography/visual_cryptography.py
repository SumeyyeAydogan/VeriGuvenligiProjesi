import numpy as np
from PIL import Image
import random

class VisualCryptography:
    def __init__(self, image_path):
        """
        (3,3) görsel şifreleme için sınıf başlatıcı.
        
        Bu sınıf, gri seviye bir görüntüyü alıp (3,3) görsel şifreleme şeması kullanarak
        3 adet pay görüntüsüne böler. Pay görüntüleri tek başlarına anlam ifade etmezken,
        üst üste konulduklarında orijinal görüntüyü ortaya çıkarır.
        
        Args:
            image_path: Giriş görüntüsünün yolu (gri seviye görüntü)
        """
        self.original_image = Image.open(image_path).convert('L')
        self.width, self.height = self.original_image.size
        self.dithered_image = None
        self.shares = []

    def apply_dithering(self):
        """
        Gri seviye görüntüyü siyah-beyaz (binary) formata dönüştürür.
        
        Bu metod basit bir threshold (eşik değeri) yaklaşımı kullanır:
        - 128'den büyük piksel değerleri beyaz (255) olur
        - 128'den küçük veya eşit piksel değerleri siyah (0) olur
        
        Returns:
            PIL.Image: Binary formata dönüştürülmüş görüntü
        """
        img_array = np.array(self.original_image)
        threshold = 128
        img_array = ((img_array > threshold) * 255).astype(np.uint8)
        self.dithered_image = Image.fromarray(img_array)
        return self.dithered_image

    def generate_random_pattern(self):
        """
        2x2'lik rastgele bir desen oluşturur.
        Desende tam olarak 2 siyah (1) ve 2 beyaz (0) piksel bulunur.
        
        Returns:
            list: 2x2'lik rastgele desen
        """
        # 2x2 matris için tüm olası 2 siyah - 2 beyaz kombinasyonları
        possible_patterns = [
            [[1,1,0,0]], [[1,0,1,0]], [[1,0,0,1]],
            [[0,1,1,0]], [[0,1,0,1]], [[0,0,1,1]]
        ]
        pattern = random.choice(possible_patterns)
        # Satır içinde rastgele karıştır
        pattern = np.array(pattern[0]).reshape(2, 2)
        return pattern.tolist()

    def generate_complementary_pattern(self, pattern):
        """
        Verilen desenin tamamlayıcısını oluşturur (0'lar 1, 1'ler 0 olur).
        
        Args:
            pattern: 2x2'lik orijinal desen
            
        Returns:
            list: 2x2'lik tamamlayıcı desen
        """
        return [[1-pattern[i][j] for j in range(2)] for i in range(2)]

    def generate_shares(self):
        """
        Binary görüntüyü (3,3) görsel şifreleme şeması kullanarak 3 paya böler.
        
        Her bir piksel 2x2'lik alt piksellere genişletilir ve rastgele paylaşım 
        desenleri kullanılarak şifrelenir. Her piksel için yeni rastgele desenler
        oluşturulur ve paylar arasında bilgi sızıntısı olmaması sağlanır.
        
        Returns:
            list: 3 adet pay görüntüsü (PIL.Image formatında)
        """
        if self.dithered_image is None:
            self.apply_dithering()

        # RGBA formatında 3 pay oluştur
        share1 = np.zeros((self.height*2, self.width*2, 4), dtype=np.uint8)
        share2 = np.zeros((self.height*2, self.width*2, 4), dtype=np.uint8)
        share3 = np.zeros((self.height*2, self.width*2, 4), dtype=np.uint8)

        binary_image = np.array(self.dithered_image) // 255

        for y in range(self.height):
            for x in range(self.width):
                y2, x2 = y*2, x*2
                
                if binary_image[y, x] == 0:  # Siyah piksel
                    # Her pay için rastgele ve birbirinden bağımsız desenler
                    pattern1 = self.generate_random_pattern()
                    pattern2 = self.generate_random_pattern()
                    pattern3 = self.generate_random_pattern()
                else:  # Beyaz piksel
                    # İlk pay için rastgele desen
                    pattern1 = self.generate_random_pattern()
                    # İkinci pay için ilk payın tamamlayıcısı
                    pattern2 = self.generate_complementary_pattern(pattern1)
                    # Üçüncü pay için yeni rastgele desen
                    pattern3 = self.generate_random_pattern()
                
                # Her pay için 2x2 alt pikselleri ayarla
                for i in range(2):
                    for j in range(2):
                        # Pay 1
                        alpha_value = 255 if pattern1[i][j] else 0
                        share1[y2+i,x2+j] = [0,0,0,alpha_value]
                        
                        # Pay 2
                        alpha_value = 255 if pattern2[i][j] else 0
                        share2[y2+i,x2+j] = [0,0,0,alpha_value]
                        
                        # Pay 3
                        alpha_value = 255 if pattern3[i][j] else 0
                        share3[y2+i,x2+j] = [0,0,0,alpha_value]

        self.shares = [
            Image.fromarray(share1, 'RGBA'),
            Image.fromarray(share2, 'RGBA'),
            Image.fromarray(share3, 'RGBA')
        ]
        return self.shares

    def combine_shares(self):
        """
        3 payı birleştirerek orijinal görüntüyü elde eder.
        
        Bu işlem, gerçek hayatta payların asetat kağıtlara basılıp
        üst üste konulmasını simüle eder. Paylar OR işlemi ile
        birleştirilir.
        
        Returns:
            PIL.Image: Birleştirilmiş görüntü
            
        Raises:
            ValueError: Eğer paylar henüz oluşturulmamışsa
        """
        if not self.shares:
            raise ValueError("Önce paylar oluşturulmalı!")

        # Payları numpy array'e dönüştür (sadece alpha kanalını kullan)
        share_arrays = [np.array(share)[:,:,3] == 255 for share in self.shares]
        
        # Mantıksal OR işlemi ile payları birleştir
        combined = share_arrays[0]
        for share in share_arrays[1:]:
            combined = np.logical_or(combined, share)
        
        # RGBA formatında sonuç oluştur
        result = np.zeros((combined.shape[0], combined.shape[1], 4), dtype=np.uint8)
        result[combined] = [0, 0, 0, 255]  # Siyah noktalar
        result[~combined] = [255, 255, 255, 255]  # Beyaz alanlar
        
        return Image.fromarray(result, 'RGBA')

    def save_shares(self, output_dir):
        """
        Pay görüntülerini belirtilen dizine kaydeder.
        
        Args:
            output_dir: Payların kaydedileceği dizin yolu
            
        Raises:
            ValueError: Eğer paylar henüz oluşturulmamışsa
        """
        if not self.shares:
            raise ValueError("Önce paylar oluşturulmalı!")
            
        for i, share in enumerate(self.shares, 1):
            share.save(f"{output_dir}/share_{i}.png")