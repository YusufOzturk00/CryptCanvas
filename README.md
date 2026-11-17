#  CryptCanvas v1.0

> **AI Destekli Gizli Mesajlaşma Uygulaması** — Sanatın altına gizli mesajlar saklayın.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Aktif-brightgreen.svg)]()

---

## 📖 Proje Hakkında

**CryptCanvas**, **steganografi (gizli yazılım)**, **yapay zeka** ve **modern kriptografi**'yi birleştiren bir gizli mesajlaşma uygulamasıdır. Mesajlarınızı AI tarafından üretilen benzersiz sanat eserlerinin piksel derinliklerine, askeri standartlarda şifreleme ile gizler.

> *"Her fırça vuruşunda bir sır..."*

---

## ✨ Özellikler

| Özellik | Açıklama |
|---------|----------|
| 🔐 **AES-256-CBC Şifreleme** | Her mesaj için benzersiz 12 karakterli şifre, rastgele IV ile semantik güvenlik |
| 🎨 **AI Görsel Üretimi** | Mesaj içeriğinden prompt türeterek Picsum Photos API ile benzersiz görseller |
| 🖼️ **LSB Steganografi** | RGB kanallarının en az anlamlı bitlerine mesaj gömme (PNG lossless) |
| 🖥️ **Çift Arayüz** | Terminal (CLI) ve Modern Web (Streamlit) |
| 📦 **Bağımsız Modüller** | Şifreleme, Steganografi, AI Görsel - her biri bağımsız kullanabilir |
| 🇹🇷 **Türkçe Arayüz** | Tamamen Türkçe kullanıcı deneyimi |

---

## 🏗️ Mimari

```
CryptCanvas/
├── app.py                 # CLI (Terminal) arayüzü
├── web_app.py             # Streamlit Web arayüzü
├── images/                # Girdi görselleri (AI üretimi)
├── output/                # Mesaj gizlenmiş çıkış görselleri
└── modules/
    ├── __init__.py
    ├── encryption.py      # AES-256 şifreleme/çözme
    ├── steganography.py   # LSB steganografi (gizle/çıkar)
    └── ai_image.py        # AI görsel üretimi (Picsum Photos)
```

---

## 🔄 Nasıl Çalışır?

### 📤 **Gönderici (Mesaj Gizleme)**
```mermaid
graph LR
    A[Mesaj Yaz] --> B[Otomatik Şifre Üret]
    B --> C[AES-256 Şifrele]
    C --> D[AI Görsel Üret]
    D --> E[LSB ile Gizle]
    E --> F[Stego-Görsel + Şifre]
```

1. Kullanıcı gizli mesajı yazar
2. Sistem **12 karakterli benzersiz şifre** üretir
3. Mesaj **AES-256-CBC** ile şifrelenir → Base64
4. AI, mesajın anahtar kelimelerinden **sanatsal görsel** üretir
5. Şifreli veri **LSB yöntemiyle** pikselin RGB kanallarına gizlenir
6. Çıktı: `output/gizli_mesaj_<timestamp>.png` + **şifre** (ayrı kanaldan paylaşılmalı)

### 📥 **Alıcı (Mesaj Çözme)**
```mermaid
graph LR
    A[Görsel Yükle] --> B[Şifre Gir]
    B --> C[LSB Çıkar]
    C --> D[AES-256 Çöz]
    D --> E[Orijinal Mesaj]
```

1. Stego-görsel yüklenir
2. Gönderenden alınan şifre girilir
3. Piksellerden Base64 veri **LSB ile çıkarılır**
4. **AES-256** ile şifre çözülür
5. Orijinal mesaj ortaya çıkar

---

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- pip

### Bağımlılıklar
```bash
pip install pycryptodome pillow requests streamlit
```

### Hızlı Başlangıç
```bash
# 1. Projeyi klonlayın
git clone <repo-url>
cd CryptCanvas

# 2. Bağımlılıkları kurun
pip install -r requirements.txt

# 3a. Terminal versiyonu
python app.py

# 3b. Web versiyonu
streamlit run web_app.py
```

> **Not:** `requirements.txt` dosyası yoksa yukarıdaki `pip install` komutunu kullanın.

---

## 💻 Kullanım

### 1. Terminal Arayüzü (CLI)
```bash
python app.py
```
```
╔══════════════════════════════════════════════╗
║          🎨 CryptCanvas v1.0                 ║
║     AI Gizli Mesajlaşma Uygulaması           ║
╚══════════════════════════════════════════════╝

📋 MENÜ:
  1. 📤 Gizli Mesaj Gönder (Gönderen)
  2. 📥 Gizli Mesaj Çöz (Alıcı)
  3. 🚪 Çıkış
```

### 2. Web Arayüzü (Streamlit)
```bash
streamlit run web_app.py
```
Tarayıcınızda `http://localhost:8501` açılır.

**Sekmeler:**
- 📤 **Gizli Mesaj Gönder** — Mesaj yazın, boyut seçin, indirin
- 📥 **Gizli Mesaj Çöz** — Görsel yükleyin, şifre girin, okuyun

---

## 🔐 Güvenlik Detayları

| Bileşen | Standard | Açıklama |
|---------|----------|----------|
| **Şifreleme** | AES-256-CBC | NIST onaylı, askeri standart |
| **Anahtar Türetme** | SHA-256 | Şifre → 256-bit anahtar (KDF) |
| **IV** | OS Random (16 byte) | Her şifrelemede benzersiz (semantik güvenlik) |
| **Encoding** | Base64 | IV + şifreli veri tek string'de |
| **Steganografi** | LSB (1-bit/kanal) | Görsel kalitesini bozmaz, PNG gerekli |
| **Mesaj Sonu** | `###SON###` | 9 byte sınırlayıcı |

> ⚠️ **Önemli:** Şifre **sadece bir kez** gösterilir. Kaybedilirse mesaj **asla** çözülemez. Şifreyi güvenli kanalla (Signal, PGP e-posta, fiziksel) paylaşın.

---

## 🧪 Modül Testleri

Her modül bağımsız test edilebilir:

```bash
# Şifreleme testi
python -c "
from modules.encryption import sifre_uret, mesaj_sifrele, mesaj_coz
s = sifre_uret()
e = mesaj_sifrele('merhaba dünya', s)
print('Şifre:', s)
print('Çözülmüş:', mesaj_coz(e, s))
"

# Steganografi testi
python -c "
from modules.steganography import mesaj_gizle, mesaj_cikar
from PIL import Image
img = Image.new('RGB', (200, 200), 'white')
img.save('test.png')
mesaj_gizle('test.png', 'gizli veri', 'out.png')
print('Çıkarılan:', mesaj_cikar('out.png'))
"

# AI Görsel testi
python -c "
from modules.ai_image import gorsel_uret
gorsel_uret('test mesajı', 'images/test_ai.png')
print('Görsel üretildi: images/test_ai.png')
"
```

---

## 📸 Ekran Görüntüleri

### Web Arayüzü - Gönderme Sekmesi
> Mesaj yazın, boyut seçin, "Gizli Görsel Oluştur" butonuna basın. Şifre ekranda gösterilir, görsel indirilebilir.

### Web Arayüzü - Çözme Sekmesi
> Görseli sürükleyip bırakın, şifreyi girin, "Mesajı Çöz" deyin.

---

## ⚙️ Yapılandırma

### Görsel Boyutları (Web)
`web_app.py` içinde değiştirilebilir:
```python
genislik = st.selectbox("📐 Görsel Genişlik", [512, 768, 1024], index=2)
yukseklik = st.selectbox("📐 Görsel Yükseklik", [512, 768, 1024], index=2)
```

### Şifre Uzunluğu
`modules/encryption.py`:
```python
def sifre_uret(uzunluk=12):  # 8-32 arası önerilir
```

### AI Prompt Temaları
`modules/ai_image.py` -> `temalar` listesi düzenlenebilir.

---

## 🐛 Bilinen Sınırlamalar

| Sınırlama | Açıklama | Çözüm |
|-----------|----------|-------|
| **Mesaj uzunluğu** | Görsel piksel sayısına bağlı (≈ piksel×3/8 byte) | Daha büyük görsel kullanın (1024×1024 ≈ 390KB metin) |
| **Sadece PNG** | JPEG sıkıştırma LSB'yi bozar | Çıktı her zaman PNG |
| **API Bağımlılığı** | Picsum Photos internet gerektirir | Offline: `varsayilan_gorsel_olustur()` devreye girer |
| **Şifre kaybı** | Geri getirilemez | Yedek alın, güvenli saklayın |

---

## 🛣️ Yol Haritası (Roadmap)

- [ ] **Drag & Drop** CLI için dosya argümanları (`python app.py -e mesaj.txt -o out.png`)
- [ ] **Batch işleme** — Toplu görsel işleme
- [ ] **Parola yöneticisi** entegrasyonu (Bitwarden, KeePass)
- [ ] **QR kod** ile şifre paylaşımı
- [ ] **Mobil uyumlu** PWA versiyonu
- [ ] **İngilizce** dil desteği
- [ ] **Docker** imajı
- [ ] **Unit testler** (pytest)

---

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request açın

### Kod Standartları
- **Python 3.8+** type hints tercih edilir
- **Docstring** formatı: Google/NumPy style
- **Modülerlik**: Her modül tek sorumluluk
- **Türkçe** yorumlar ve docstring'ler

---

## 📄 Lisans

Bu proje **MIT Lisansı** altında lisanslanmıştır. Detaylar için [`LICENSE`](LICENSE) dosyasına bakın.

```
MIT License

Copyright (c) 2026 CryptCanvas

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🙏 Teşekkürler

- **[Picsum Photos](https://picsum.photos/)** — Ücretsiz, API key'siz görsel API'si
- **[PyCryptodome](https://pycryptodome.readthedocs.io/)** — Güçlü kriptografi kütüphanesi
- **[Pillow](https://pillow.readthedocs.io/)** — Görsel işleme
- **[Streamlit](https://streamlit.io/)** — Harika web arayüz framework'ü

---

## 📞 İletişim & Destek

- **Issues**: [GitHub Issues](https://github.com/<kullanici>/CryptCanvas/issues) — Hata raporları, öneriler
- **Discussions**: [GitHub Discussions](https://github.com/<kullanici>/CryptCanvas/discussions) — Sorular, fikirler

---

<div align="center">

**⭐ Bu projeyi beğendiyseniz yıldızlayın!**

Made with 🎨 + 🔒 in Türkiye

</div>