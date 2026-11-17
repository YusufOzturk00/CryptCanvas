"""
CryptCanvas - Steganografi Modülü
Resmin piksellerine mesaj gizler ve çıkarır (LSB Yöntemi)
"""

from PIL import Image


def mesaj_gizle(image_path, mesaj, output_path):
    """
    Bir resmin içine gizli mesaj gömer.
    LSB (Least Significant Bit) yöntemi kullanır.
    """
    img = Image.open(image_path)
    img = img.convert("RGB")
    pixels = list(img.getdata())

    # Mesajın sonuna bitiş işareti ekle
    mesaj += "###SON###"
    binary_mesaj = ''.join(format(ord(c), '08b') for c in mesaj)

    if len(binary_mesaj) > len(pixels) * 3:
        raise ValueError("Mesaj bu resim için çok uzun! Daha büyük bir resim kullanın.")

    yeni_pixels = []
    bit_index = 0

    for pixel in pixels:
        yeni_pixel = list(pixel)
        for i in range(3):  # R, G, B kanalları
            if bit_index < len(binary_mesaj):
                # Son biti mesajın biti ile değiştir
                yeni_pixel[i] = (yeni_pixel[i] & ~1) | int(binary_mesaj[bit_index])
                bit_index += 1
        yeni_pixels.append(tuple(yeni_pixel))

    # Yeni resmi oluştur ve kaydet
    yeni_img = Image.new(img.mode, img.size)
    yeni_img.putdata(yeni_pixels)
    yeni_img.save(output_path, "PNG")
    print(f"✅ Mesaj başarıyla gizlendi: {output_path}")
    return output_path


def mesaj_cikar(image_path):
    """
    Resmin piksellerinden gizli mesajı çıkarır.
    """
    img = Image.open(image_path)
    img = img.convert("RGB")
    pixels = list(img.getdata())

    binary_mesaj = ""
    for pixel in pixels:
        for i in range(3):  # R, G, B kanalları
            binary_mesaj += str(pixel[i] & 1)

    # Binary'den metne çevir
    mesaj = ""
    for i in range(0, len(binary_mesaj), 8):
        byte = binary_mesaj[i:i+8]
        if len(byte) == 8:
            karakter = chr(int(byte, 2))
            mesaj += karakter
            # Bitiş işaretini kontrol et
            if mesaj.endswith("###SON###"):
                return mesaj[:-9]  # Bitiş işaretini kaldır

    return "⚠️ Gizli mesaj bulunamadı!"


# Test
if __name__ == "__main__":
    # Test için basit bir resim oluştur
    test_img = Image.new("RGB", (100, 100), color="blue")
    test_img.save("test_resim.png")

    mesaj_gizle("test_resim.png", "Merhaba bu gizli mesaj!", "test_output.png")
    sonuc = mesaj_cikar("test_output.png")
    print(f"Çıkarılan mesaj: {sonuc}")