class SharePatterns:
    @staticmethod
    def get_patterns(pixel_value):
        """
        Piksel değerine göre uygun desenleri döndür
        Args:
            pixel_value: 1 (beyaz) veya 0 (siyah)
        Returns:
            list: Olası desenler listesi
        """
        if pixel_value == 1:  # Beyaz piksel
            return [
                [[1, 0], [0, 1]],
                [[0, 1], [1, 0]]
            ]
        else:  # Siyah piksel
            return [
                [[1, 1], [0, 0]],
                [[0, 0], [1, 1]],
                [[1, 0], [1, 0]],
                [[0, 1], [0, 1]]
            ] 