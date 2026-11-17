"""
CryptCanvas - AI Görsel Üretim Modülü
Birden fazla ücretsiz API ile görsel üretir
"""

import requests
import urllib.parse
import os
import random
import time


def mesajdan_prompt_olustur(mesaj):
    """Mesajdan güvenli prompt oluşturur."""
    kelimeler = []
    for kelime in mesaj.split():
        temiz = ''.join(c for c in kelime if c.isalpha())
        if len(temiz) >= 2:
            kelimeler.append(temiz)

    temalar = [
        "peaceful mountain landscape sunset",
        "beautiful ocean waves beach",
        "colorful garden butterflies spring",
        "starry night sky city lights",
        "autumn forest golden leaves path",
        "snowy village winter cozy",
        "tropical beach palm trees paradise",
        "magical waterfall green forest nature",
        "field of sunflowers blue sky",
        "cherry blossom japanese garden"
    ]

    if kelimeler:
        konu = ' '.join(kelimeler)
        prompt = f"beautiful artistic painting of {konu}, vibrant colors, detailed, masterpiece"
    else:
        tema = random.choice(temalar)
        prompt = f"beautiful artistic painting of {tema}, vibrant colors, detailed, masterpiece"

    return prompt


def gorsel_uret(mesaj, output_path, genislik=1024, yukseklik=1024):
    """Birden fazla ücretsiz API deneyerek görsel üretir."""
    print("🎨 AI görsel üretiliyor... (bu birkaç saniye sürebilir)")

    prompt = mesajdan_prompt_olustur(mesaj)
    print(f"   Prompt: {prompt[:80]}...")

    
    # ===== YÖNTEM 5: Lorem Picsum (Rastgele kaliteli fotoğraf) =====
    try:
        print("\n   🔄 3 Picsum Photos deneniyor...")
        url = f"https://picsum.photos/{genislik}/{yukseklik}"

        response = requests.get(url, timeout=60, allow_redirects=True)

        if response.status_code == 200 and len(response.content) > 10000:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            # JPEG'i PNG'ye çevir (steganografi için PNG gerekli)
            from PIL import Image
            img = Image.open(output_path).convert("RGB")
            img.save(output_path, "PNG")
            print(f"   ✅ Görsel indirildi (Picsum): {output_path}")
            return output_path
        else:
            print(f"   ⚠️  Picsum yanıt kodu: {response.status_code}")

    except Exception as e:
        print(f"   ⚠️  Yöntem 5 başarısız: {e}")

    # Hiçbiri çalışmazsa
    print("\n   ❌ Tüm API'ler başarısız, yedek görsel oluşturulacak.")
    return None


def varsayilan_gorsel_olustur(output_path):
    """API çalışmazsa yedek gradient görsel oluşturur."""
    from PIL import Image
    import random

    img = Image.new("RGB", (1024, 1024))
    pixels = img.load()

    paletler = [
        ((30, 80), (50, 120), (150, 230)),
        ((150, 220), (50, 100), (80, 160)),
        ((50, 120), (150, 220), (50, 100)),
        ((200, 240), (100, 180), (30, 80)),
    ]

    r_range, g_range, b_range = random.choice(paletler)
    r_s = random.randint(*r_range)
    g_s = random.randint(*g_range)
    b_s = random.randint(*b_range)

    for y in range(1024):
        for x in range(1024):
            n = random.randint(-5, 5)
            r = max(0, min(255, r_s + (x * 80 // 1024) + n))
            g = max(0, min(255, g_s + (y * 80 // 1024) + n))
            b = max(0, min(255, b_s + ((x + y) * 60 // 2048) + n))
            pixels[x, y] = (r, g, b)

    img.save(output_path, "PNG")
    print(f"   ✅ Yedek görsel oluşturuldu: {output_path}")
    return output_path


# Test
if __name__ == "__main__":
    os.makedirs("images", exist_ok=True)
    sonuc = gorsel_uret(
        mesaj="20.02.2026 23.30 Ankara",
        output_path="images/test_ai_gorsel.png"
    )
    if sonuc is None:
        varsayilan_gorsel_olustur("images/test_ai_gorsel.png")