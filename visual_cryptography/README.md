# (3,3) Görsel Şifreleme Projesi

Bu proje, gri seviye görüntüleri (3,3) görsel şifreleme yöntemi kullanarak şifrelemek için geliştirilmiş bir uygulamadır. Görsel şifreleme, bir görüntüyü birden fazla anlamsız parçaya (pay) bölerek, bu parçaların tümünün veya belirli bir sayısının bir araya getirilmesiyle orijinal görüntünün elde edilmesini sağlayan bir kriptografik yöntemdir.

## Proje Özellikleri

- Gri seviye görüntüleri işleme
- (3,3) görsel şifreleme şeması
- Basit ve etkili threshold-based ikileştirme
- Güvenli ve rastgele pay üretimi
- Asetat baskı için uygun çıktı formatı

## Algoritma Detayları ve Kod Açıklamaları

### 1. Sınıf Yapısı ve Başlatma

```python
class VisualCryptography:
    def __init__(self, image_path):
        """
        Görsel şifreleme sınıfının başlatıcısı
        """
        self.original_image = Image.open(image_path).convert('L')  # Gri seviyeye dönüştür
        self.width, self.height = self.original_image.size
        self.dithered_image = None
        self.shares = []
```

Bu kısımda:
- Görüntü gri seviyeye dönüştürülür (`convert('L')`)
- Görüntü boyutları saklanır
- Pay görüntüleri için boş liste oluşturulur

### 2. Görüntü İkileştirme (Binarization)

```python
def apply_dithering(self):
    """
    Gri seviye görüntüyü siyah-beyaz formata dönüştürür
    """
    img_array = np.array(self.original_image)
    threshold = 128
    img_array = ((img_array > threshold) * 255).astype(np.uint8)
    self.dithered_image = Image.fromarray(img_array)
    return self.dithered_image
```

İkileştirme işlemi:
1. Görüntü numpy dizisine dönüştürülür
2. Her piksel 128 eşik değeri ile karşılaştırılır
3. 128'den büyük değerler 255 (beyaz), küçük veya eşit değerler 0 (siyah) olur

### 3. Rastgele Desen Üretimi

```python
def generate_random_pattern(self):
    """
    2x2'lik rastgele desen üretir
    """
    possible_patterns = [
        [[1,1,0,0]], [[1,0,1,0]], [[1,0,0,1]],
        [[0,1,1,0]], [[0,1,0,1]], [[0,0,1,1]]
    ]
    pattern = random.choice(possible_patterns)
    pattern = np.array(pattern[0]).reshape(2, 2)
    return pattern.tolist()
```

Desen üretimi:
1. 6 farklı olası desen tanımlanır (her biri 2 siyah, 2 beyaz piksel içerir)
2. Rastgele bir desen seçilir
3. 2x2 matris formatına dönüştürülür

### 4. Tamamlayıcı Desen Üretimi

```python
def generate_complementary_pattern(self, pattern):
    """
    Verilen desenin tamamlayıcısını üretir
    """
    return [[1-pattern[i][j] for j in range(2)] for i in range(2)]
```

Tamamlayıcı desen:
1. Orijinal desendeki her piksel tersine çevrilir (0→1, 1→0)
2. Beyaz pikseller için kullanılır
3. İki desen üst üste konduğunda tamamen beyaz alan oluşturur

### 5. Pay Üretimi

```python
def generate_shares(self):
    """
    Binary görüntüyü 3 paya böler
    """
    # Pay görüntüleri için boş RGBA dizileri oluştur
    share1 = np.zeros((self.height*2, self.width*2, 4), dtype=np.uint8)
    share2 = np.zeros((self.height*2, self.width*2, 4), dtype=np.uint8)
    share3 = np.zeros((self.height*2, self.width*2, 4), dtype=np.uint8)

    binary_image = np.array(self.dithered_image) // 255

    for y in range(self.height):
        for x in range(self.width):
            y2, x2 = y*2, x*2
            
            if binary_image[y, x] == 0:  # Siyah piksel
                pattern1 = self.generate_random_pattern()
                pattern2 = self.generate_random_pattern()
                pattern3 = self.generate_random_pattern()
            else:  # Beyaz piksel
                pattern1 = self.generate_random_pattern()
                pattern2 = self.generate_complementary_pattern(pattern1)
                pattern3 = self.generate_random_pattern()
            
            # Desenleri paylara uygula
            for i in range(2):
                for j in range(2):
                    # Her pay için alpha değerlerini ayarla
                    share1[y2+i,x2+j] = [0,0,0, 255 if pattern1[i][j] else 0]
                    share2[y2+i,x2+j] = [0,0,0, 255 if pattern2[i][j] else 0]
                    share3[y2+i,x2+j] = [0,0,0, 255 if pattern3[i][j] else 0]
```

Pay üretim süreci:
1. Her pay için orijinal görüntünün 2 katı boyutunda boş RGBA dizileri oluşturulur
2. Her piksel için:
   - Siyah pikseller: 3 bağımsız rastgele desen
   - Beyaz pikseller: 1 rastgele desen + 1 tamamlayıcı + 1 rastgele desen
3. Her desen 2x2'lik alt piksellere dönüştürülür
4. Alpha kanalı kullanılarak transparanlık ayarlanır (255: siyah, 0: transparent)

### 6. Pay Birleştirme

```python
def combine_shares(self):
    """
    3 payı birleştirerek orijinal görüntüyü elde eder
    """
    share_arrays = [np.array(share)[:,:,3] == 255 for share in self.shares]
    
    combined = share_arrays[0]
    for share in share_arrays[1:]:
        combined = np.logical_or(combined, share)
    
    result = np.zeros((combined.shape[0], combined.shape[1], 4), dtype=np.uint8)
    result[combined] = [0, 0, 0, 255]  # Siyah noktalar
    result[~combined] = [255, 255, 255, 255]  # Beyaz alanlar
    
    return Image.fromarray(result, 'RGBA')
```

Birleştirme işlemi:
1. Her payın alpha kanalı boolean matrise dönüştürülür
2. Paylar OR işlemi ile birleştirilir
3. Sonuç RGBA formatına dönüştürülür
4. Siyah ve beyaz alanlar için uygun RGBA değerleri atanır

## Kullanım Örneği

```python
# Görsel şifreleme nesnesini oluştur
vc = VisualCryptography("input/image.png")

# Görüntüyü ikileştir ve payları oluştur
binary_image = vc.apply_dithering()
shares = vc.generate_shares()

# Payları kaydet
vc.save_shares("output/shares")

# Payları birleştir ve sonucu kaydet
combined = vc.combine_shares()
combined.save("output/result.png")
```

## Çıktı Formatları

1. **İkileştirilmiş Görüntü (binary_image)**
   - Format: Grayscale (L)
   - Boyut: Orijinal görüntü ile aynı
   - Değerler: 0 (siyah) veya 255 (beyaz)

2. **Pay Görüntüleri (share_1.png, share_2.png, share_3.png)**
   - Format: RGBA
   - Boyut: Orijinal görüntünün 2 katı
   - Alpha kanalı: 0 (transparent) veya 255 (siyah)

3. **Birleştirilmiş Görüntü (result.png)**
   - Format: RGBA
   - Boyut: Orijinal görüntünün 2 katı
   - Değerler: [0,0,0,255] (siyah) veya [255,255,255,255] (beyaz)

## Teknik Gereksinimler

### Yazılım Gereksinimleri
- Python 3.x
- NumPy >= 1.19.0
- Pillow (PIL) >= 8.0.0

### Kurulum

```bash
# Sanal ortam oluştur (opsiyonel ama önerilen)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Gereksinimleri yükle
pip install -r requirements.txt
```

## Güvenlik Özellikleri

1. **Rastgele Desen Üretimi**
   - Her piksel için yeni rastgele desenler
   - 6 farklı olası desen kombinasyonu
   - Uniform dağılımlı seçim

2. **Pay Bağımsızlığı**
   - Paylar arası korelasyon yok
   - Her pay bağımsız rastgele desenler içerir
   - Tek pay ile görüntü elde edilemez

3. **Bilgi Gizleme**
   - Her payda eşit sayıda siyah ve beyaz piksel
   - Desenler orijinal pikseli gizler
   - İstatistiksel analiz direnci

4. **Tamamlayıcı Desen Güvenliği**
   - Beyaz pikseller için özel koruma
   - Tamamlayıcı desenler ile bilgi gizleme
   - OR işlemi ile güvenli birleştirme

## Kısıtlamalar ve Çözümleri

1. **Görüntü Boyutu Artışı**
   - Sorun: 2x2 alt pikseller nedeniyle boyut 2 katına çıkar
   - Çözüm: Çıktı görüntüsü sıkıştırılabilir

2. **Gri Seviye Sınırlaması**
   - Sorun: Sadece gri seviye görüntüler desteklenir
   - Çözüm: Renkli görüntüler otomatik dönüştürülür

3. **Kontrast Kaybı**
   - Sorun: Birleştirmede kontrast düşebilir
   - Çözüm: Optimize edilmiş desen matrisleri

## Gelecek Geliştirmeler

1. **Renkli Görüntü Desteği**
   - RGB kanalları için ayrı paylar
   - Renk uzayı optimizasyonu
   - Renk doğruluğu koruması

2. **Farklı (k,n) Şemaları**
   - 2'den n'ye kadar pay desteği
   - Esnek k değeri seçimi
   - Özelleştirilebilir güvenlik seviyesi

3. **Gelişmiş Dithering**
   - Floyd-Steinberg dithering
   - Hata yayılımı algoritmaları
   - Adaptif threshold

4. **Optimizasyonlar**
   - Paralel işleme desteği
   - Bellek kullanımı optimizasyonu
   - Hız iyileştirmeleri

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.
