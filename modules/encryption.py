"""
CryptCanvas - Şifreleme Modülü
AES-256 ile mesaj şifreleme ve çözme
"""

import hashlib
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import secrets
import string

def sifre_uret(uzunluk=12):  # 12 karakterli güçlü şifre üretir
    alfabe = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alfabe) for _ in range(uzunluk))

# ... kalan kodun aynı: anahtar_olustur, mesaj_sifrele, mesaj_coz ...

def anahtar_olustur(sifre):
    """
    Kullanıcının girdiği şifreden 256-bit AES anahtarı üretir.
    """
    return hashlib.sha256(sifre.encode('utf-8')).digest()


def mesaj_sifrele(mesaj, sifre):
    """
    Mesajı AES-256-CBC ile şifreler.
    Dönen değer: base64 encoded string (IV + şifreli veri)
    """
    anahtar = anahtar_olustur(sifre)
    iv = os.urandom(16)  # Rastgele IV (Initialization Vector)
    cipher = AES.new(anahtar, AES.MODE_CBC, iv)

    # Mesajı şifrele
    padded_mesaj = pad(mesaj.encode('utf-8'), AES.block_size)
    sifreli_veri = cipher.encrypt(padded_mesaj)

    # IV + şifreli veriyi birleştir ve base64 ile encode et
    sonuc = base64.b64encode(iv + sifreli_veri).decode('utf-8')
    return sonuc


def mesaj_coz(sifreli_mesaj, sifre):
    """
    AES-256-CBC ile şifrelenmiş mesajı çözer.
    """
    try:
        anahtar = anahtar_olustur(sifre)

        # Base64 decode
        veri = base64.b64decode(sifreli_mesaj)

        # IV ve şifreli veriyi ayır
        iv = veri[:16]
        sifreli_veri = veri[16:]

        # Şifreyi çöz
        cipher = AES.new(anahtar, AES.MODE_CBC, iv)
        cozulmus = unpad(cipher.decrypt(sifreli_veri), AES.block_size)

        return cozulmus.decode('utf-8')
    except (ValueError, KeyError):
        return "❌ Yanlış şifre! Mesaj çözülemedi."


# Test
if __name__ == "__main__":
    orijinal = "Bu çok gizli bir mesajdır!"
    sifre = "parola123"

    sifreli = mesaj_sifrele(orijinal, sifre)
    print(f"Orijinal:  {orijinal}")
    print(f"Şifreli:   {sifreli}")

    cozulmus = mesaj_coz(sifreli, sifre)
    print(f"Çözülmüş:  {cozulmus}")

    # Yanlış şifre ile dene
    yanlis = mesaj_coz(sifreli, "yanlis_sifre")
    print(f"Yanlış şifre: {yanlis}")