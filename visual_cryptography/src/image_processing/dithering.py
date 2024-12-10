import numpy as np
from PIL import Image

class FloydSteinbergDithering:
    def apply(self, image, threshold=128):
        """
        Floyd-Steinberg dithering algoritması
        Args:
            image: Giriş görüntüsü (PIL Image)
            threshold: Eşik değeri
        Returns:
            PIL Image: Dither uygulanmış görüntü
        """
        img_array = np.array(image, dtype=float)
        height, width = img_array.shape
        output = np.zeros_like(img_array)

        for y in range(height-1):
            for x in range(width-1):
                old_pixel = img_array[y, x]
                new_pixel = 255 if old_pixel > threshold else 0
                output[y, x] = new_pixel
                
                error = old_pixel - new_pixel
                
                # Hata yayılımı
                if x + 1 < width:
                    img_array[y, x+1] += error * 7/16
                if y + 1 < height:
                    if x > 0:
                        img_array[y+1, x-1] += error * 3/16
                    img_array[y+1, x] += error * 5/16
                    if x + 1 < width:
                        img_array[y+1, x+1] += error * 1/16

        return Image.fromarray(output.astype(np.uint8)) 