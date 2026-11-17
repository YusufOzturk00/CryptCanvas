"""
CryptCanvas - Streamlit Web Arayüzü
Cloud Shell üzerinden çalışmak için tasarlandı
"""

import streamlit as st
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.steganography import mesaj_gizle, mesaj_cikar
from modules.encryption import mesaj_sifrele, mesaj_coz, sifre_uret
from modules.ai_image import gorsel_uret, varsayilan_gorsel_olustur

# Klasörleri oluştur
os.makedirs("images", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Sayfa ayarları
st.set_page_config(
    page_title="CryptCanvas - AI Gizli Mesajlaşma",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #1a1a2e, #16213e, #0f3460);
        border-radius: 15px;
        margin-bottom: 25px;
        color: white;
    }
    .success-box {
        background: #1a3a1a;
        border: 1px solid #2ecc71;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .password-box {
        background: #1a1a3a;
        border: 2px solid #3498db;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        color: #3498db;
        letter-spacing: 3px;
        margin: 15px 0;
    }
    .warning-box {
        background: #3a2a1a;
        border: 1px solid #e67e22;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 50px;
        font-size: 16px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🔒 CryptCanvas v1.0</h1>
    <p>AI Destekli Gizli Mesajlaşma Uygulaması</p>
    <small>Mesajını yaz → AI görsel üretsin → Mesaj görsele gizlensin → Gönder!</small>
</div>
""", unsafe_allow_html=True)

# Tab seçimi
tab1, tab2 = st.tabs(["📤 Gizli Mesaj Gönder", "📥 Gizli Mesaj Çöz"])


# ────────────────────────��────────────────
# TAB 1: GÖNDERME MODU
# ─────────────────────────────────────────
with tab1:
    st.subheader("📤 Gizli Mesaj Oluştur")
    st.write("Mesajını yaz, biz gerisini halledelim!")

    mesaj = st.text_area(
        "✏️ Gizli mesajınızı yazın:",
        placeholder="Buraya gizlemek istediğin mesajı yaz...",
        height=120,
        key="mesaj_input"
    )

    col1, col2 = st.columns(2)
    with col1:
        genislik = st.selectbox("📐 Görsel Genişlik", [512, 768, 1024], index=2)
    with col2:
        yukseklik = st.selectbox("📐 Görsel Yükseklik", [512, 768, 1024], index=2)

    if st.button("🚀 Gizli Görsel Oluştur", key="gonder_btn", type="primary"):
        if not mesaj.strip():
            st.error("❌ Mesaj boş olamaz!")
        else:
            # Progress bar
            progress = st.progress(0)
            status = st.empty()

            # 1. Şifre üret
            status.info("🔐 Şifre oluşturuluyor...")
            progress.progress(15)
            sifre = sifre_uret()
            time.sleep(0.3)

            # 2. Şifrele
            status.info("🔒 Mesaj şifreleniyor (AES-256)...")
            progress.progress(30)
            sifreli_mesaj = mesaj_sifrele(mesaj, sifre)
            time.sleep(0.3)

            # 3. Görsel üret
            status.info("🎨 AI görsel üretiliyor...")
            progress.progress(50)
            timestamp = int(time.time())
            ai_gorsel_path = os.path.join("images", f"ai_gorsel_{timestamp}.png")
            sonuc = gorsel_uret(mesaj, ai_gorsel_path, genislik, yukseklik)

            if sonuc is None:
                status.warning("⚠️ AI görsel üretilemedi, yedek görsel kullanılıyor...")
                varsayilan_gorsel_olustur(ai_gorsel_path)

            progress.progress(75)

            # 4. Mesajı görsele göm
            status.info("🖼️ Mesaj görsele gizleniyor (LSB Steganografi)...")
            output_path = os.path.join("output", f"gizli_mesaj_{timestamp}.png")
            mesaj_gizle(ai_gorsel_path, sifreli_mesaj, output_path)
            progress.progress(100)

            status.empty()
            progress.empty()

            # Sonuç göster
            st.success("🎉 İşlem tamamlandı!")

            # Şifreyi göster
            st.markdown(f"""
            <div class="password-box">
                🔑 {sifre}
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="warning-box">
                ‼️ <strong>Bu şifreyi alıcıya iletmeyi unutmayın!</strong><br>
                Bu şifre olmadan mesaj çözülemez.
            </div>
            """, unsafe_allow_html=True)

            # Görseli göster
            col_img, col_info = st.columns([1, 1])
            with col_img:
                st.image(output_path, caption="🖼️ Gizli Görsel", use_container_width=True)
            with col_info:
                st.write("📊 **İşlem Özeti:**")
                st.write(f"- 🔐 Şifre: `{sifre}`")
                st.write(f"- 📏 Görsel: {genislik}x{yukseklik}px")
                st.write(f"- 📁 Dosya: `{output_path}`")
                st.write(f"- ⏰ Zaman: `{timestamp}`")

            # İndir butonu
            with open(output_path, "rb") as f:
                st.download_button(
                    label="⬇️ Gizli Görseli İndir",
                    data=f,
                    file_name=f"gizli_mesaj_{timestamp}.png",
                    mime="image/png",
                    use_container_width=True
                )

            # Şifreli mesajı da göster (isteğe bağlı)
            with st.expander("🔍 Teknik Detaylar (İsteğe Bağlı)"):
                st.code(f"Şifreli Mesaj: {sifreli_mesaj[:80]}...", language="text")
                st.code(f"Dosya Yolu: {output_path}", language="text")


# ─────────────────────────────────────────
# TAB 2: ÇÖZME MODU
# ─────────────────────────────────────────
with tab2:
    st.subheader("📥 Gizli Mesajı Çöz")
    st.write("Gönderilen görseli yükle ve şifreyi gir!")

    uploaded_file = st.file_uploader(
        "🖼️ Gizli görseli yükleyin:",
        type=["png"],
        key="gorsel_upload"
    )

    sifre_input = st.text_input(
        "🔐 Şifreyi girin:",
        placeholder="Göndericinin verdiği şifreyi yaz...",
        type="password",
        key="sifre_input"
    )

    if uploaded_file is not None:
        st.image(uploaded_file, caption="📎 Yüklenen Görsel", width=300)

    if st.button("🔓 Mesajı Çöz", key="coz_btn", type="primary"):
        if uploaded_file is None:
            st.error("❌ Lütfen bir görsel yükleyin!")
        elif not sifre_input.strip():
            st.error("❌ Lütfen şifreyi girin!")
        else:
            progress = st.progress(0)
            status = st.empty()

            # Görseli geçici kaydet
            status.info("🔍 Görsel analiz ediliyor...")
            progress.progress(30)
            temp_path = os.path.join("images", f"temp_{int(time.time())}.png")
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            # Steganografi ile çıkar
            sifreli_mesaj = mesaj_cikar(temp_path)
            progress.progress(60)

            # Temp dosyayı sil
            os.remove(temp_path)

            if "bulunamadı" in sifreli_mesaj:
                status.empty()
                progress.empty()
                st.error("⚠️ Bu görselde gizli mesaj bulunamadı!")
            else:
                # Şifreyi çöz
                status.info("🔓 Mesaj çözülüyor...")
                progress.progress(90)
                cozulmus = mesaj_coz(sifreli_mesaj, sifre_input)
                progress.progress(100)

                status.empty()
                progress.empty()

                if "Yanlış şifre" in cozulmus:
                    st.error(f"❌ {cozulmus}")
                else:
                    st.success("✅ Mesaj başarıyla çözüldü!")
                    st.markdown(f"""
                    <div class="success-box">
                        <h3>📨 Gizli Mesaj:</h3>
                        <p style="font-size: 18px; color: #2ecc71;">{cozulmus}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    with st.expander("🔍 Teknik Detaylar"):
                        st.code(f"Şifreli (Base64): {sifreli_mesaj[:80]}...", language="text")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>🎨 CryptCanvas v1.0 | AES-256 + LSB Steganografi</p>",
    unsafe_allow_html=True
)