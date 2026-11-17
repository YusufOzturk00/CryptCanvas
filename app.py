"""
CryptCanvas - AI Gizli Mesajlaşma Uygulaması
Her görsel için otomatik (benzersiz) şifre üretir!
"""

import os
import sys

# Modül yolunu ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.steganography import mesaj_gizle, mesaj_cikar
from modules.encryption import mesaj_sifrele, mesaj_coz, sifre_uret
from modules.ai_image import gorsel_uret, varsayilan_gorsel_olustur


def banner():
    print("""
    ╔══════════════════════════════════════════════╗
    ║          🎨 CryptCanvas v1.0                 ║
    ║     AI Gizli Mesajlaşma Uygulaması           ║
    ║                                              ���
    ║  Mesajını yaz → AI görsel üretsin →          ║
    ║  Mesaj görsele gizlensin → Gönder!           ║
    ╚══════════════════════════════════════════════╝
    """)


def mesaj_gonder_modu():
    """X kişisi: Mesaj yazıp gizli görsel oluşturur"""
    print("\n" + "="*50)
    print("📤 GİZLİ MESAJ GÖNDERME MODU")
    print("="*50)

    # 1. Mesajı al
    mesaj = input("\n✏️  Gizli mesajınızı yazın: ")
    if not mesaj.strip():
        print("❌ Mesaj boş olamaz!")
        return

    # 2. Şifre otomatik oluşturulsun!
    sifre = sifre_uret()  # Artık modülden geliyor (aşağıda kodu var)
    print(f"\n🔐 Bu görsele özel şifreniz: {sifre}\n‼️ Lütfen bu şifreyi alıcıya iletin!‼️")

    # 3. Mesajı şifrele
    print("\n🔒 Mesaj şifreleniyor...")
    sifreli_mesaj = mesaj_sifrele(mesaj, sifre)
    print(f"   Şifreli mesaj: {sifreli_mesaj[:50]}...")

    # 4. AI ile görsel üret
    ai_gorsel_path = os.path.join("images", "ai_gorsel.png")
    sonuc = gorsel_uret(mesaj, ai_gorsel_path)

    if sonuc is None:
        print("⚠️  AI görsel üretilemedi, yedek görsel kullanılıyor...")
        varsayilan_gorsel_olustur(ai_gorsel_path)

    # 5. Şifreli mesajı görsele gizle
    output_path = os.path.join("output", "gizli_mesaj_gorsel.png")
    print("\n🖼️  Mesaj görsele gizleniyor...")
    mesaj_gizle(ai_gorsel_path, sifreli_mesaj, output_path)

    print("\n" + "="*50)
    print("🎉 İŞLEM TAMAMLANDI!")
    print(f"📁 Gizli görselin yolu: {output_path}")
    print(f"🔑 Şifreniz: {sifre} (Bu şifre olmadan mesaj çözülemez!)")
    print("="*50)


def mesaj_coz_modu():
    """Y kişisi: Görseldeki gizli mesajı çözer"""
    print("\n" + "="*50)
    print("📥 GİZLİ MESAJ ÇÖZME MODU")
    print("="*50)

    # 1. Görsel yolunu al
    gorsel_path = input("\n🖼️  Gizli görselin dosya yolunu girin: ")
    if not os.path.exists(gorsel_path):
        print("❌ Dosya bulunamadı!")
        return

    # 2. Şifreyi alıcıdan al
    sifre = input("🔐 Gönderen tarafından verilen şifreyi girin: ")

    # 3. Görselden şifreli mesajı çıkar
    print("\n🔍 Görsel analiz ediliyor...")
    sifreli_mesaj = mesaj_cikar(gorsel_path)

    if "bulunamadı" in sifreli_mesaj:
        print(sifreli_mesaj)
        return

    # 4. Mesajı çöz
    print("🔓 Mesaj çözülüyor...")
    cozulmus_mesaj = mesaj_coz(sifreli_mesaj, sifre)

    print("\n" + "="*50)
    if "Yanlış şifre" in cozulmus_mesaj:
        print(f"❌ {cozulmus_mesaj}")
    else:
        print(f"✅ GİZLİ MESAJ: {cozulmus_mesaj}")
    print("="*50)


def main():
    banner()
    while True:
        print("\n📋 MENÜ:")
        print("  1. 📤 Gizli Mesaj Gönder (Gönderen)")
        print("  2. 📥 Gizli Mesaj Çöz (Alıcı)")
        print("  3. 🚪 Çıkış")
        secim = input("\nSeçiminiz (1/2/3): ").strip()
        if secim == "1":
            mesaj_gonder_modu()
        elif secim == "2":
            mesaj_coz_modu()
        elif secim == "3":
            print("\n👋 CryptCanvas'tan çıkılıyor. Güle güle!")
            break
        else:
            print("❌ Geçersiz seçim! 1, 2 veya 3 girin.")

if __name__ == "__main__":
    main()