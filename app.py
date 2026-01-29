import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- AYARLAR VE VERİTABANI KURULUMU ---
DOSYA_ADI = "akademi_veri.csv"

# Eğer dosya yoksa boş bir tane oluştur
if not os.path.exists(DOSYA_ADI):
    df_empty = pd.DataFrame(columns=["Tarih", "Öğrenci", "Eğitmen", "Ders Alanı", "Konu/Kazanım", "Performans", "Notlar"])
    df_empty.to_csv(DOSYA_ADI, index=False)

def veri_yukle():
    return pd.read_csv(DOSYA_ADI)

def veri_kaydet(yeni_veri):
    mevcut_veri = veri_yukle()
    guncel_veri = pd.concat([mevcut_veri, yeni_veri], ignore_index=True)
    guncel_veri.to_csv(DOSYA_ADI, index=False)
    return guncel_veri

# --- SAYFA TASARIMI ---
st.set_page_config(page_title="Akademi Disleksi Takip", page_icon="🧩", layout="wide")

st.title("🧩 Akademi Disleksi - Dijital Ders Takip Sistemi")
st.markdown("---")

# Yan Menü (Navigasyon)
menu = st.sidebar.radio("Menü", ["📝 Ders Girişi", "📊 Öğrenci Karnesi & Rapor", "⚙️ Ayarlar"])

# --- 1. MODÜL: DERS GİRİŞİ ---
if menu == "📝 Ders Girişi":
    st.header("Yeni Ders Kaydı Oluştur")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Bu listeleri Ayarlar kısmından veya koddan güncelleyebilirsiniz
        ogrenci_listesi = ["Ahmet Y.", "Ayşe K.", "Mehmet T.", "Zeynep B.", "Can D."]
        secilen_ogrenci = st.selectbox("Öğrenci Seçiniz", ogrenci_listesi)
        
        egitmen_adi = st.text_input("Eğitmen Adı Soyadı")
        
        ders_alani = st.selectbox("Çalışılan Alan", [
            "Okuma-Yazma (Disleksi)", 
            "Matematik (Diskalkuli)", 
            "Dikkat ve Algı", 
            "İnce Motor / Yazı (Disgrafi)",
            "Sosyal Beceriler"
        ])

    with col2:
        konu = st.text_input("Çalışılan Konu / Kazanım (Örn: b-d ayrımı)")
        
        performans = st.select_slider("Öğrenci Performansı", 
            options=["Fiziksel Yardım", "Model Olma", "Sözel İpucu", "İşaret İpucu", "Tam Bağımsız"],
            value="Sözel İpucu")
            
        notlar = st.text_area("Eğitmen Notu / Ödev Bilgisi")
        
        tarih = st.date_input("Tarih", datetime.now())

    if st.button("💾 Kaydı Tamamla", type="primary"):
        if egitmen_adi and konu:
            yeni_kayit = pd.DataFrame({
                "Tarih": [tarih],
                "Öğrenci": [secilen_ogrenci],
                "Eğitmen": [egitmen_adi],
                "Ders Alanı": [ders_alani],
                "Konu/Kazanım": [konu],
                "Performans": [performans],
                "Notlar": [notlar]
            })
            veri_kaydet(yeni_kayit)
            st.success(f"✅ {secilen_ogrenci} için ders kaydı başarıyla eklendi!")
        else:
            st.warning("⚠️ Lütfen Eğitmen Adı ve Konu kısımlarını boş bırakmayınız.")

# --- 2. MODÜL: RAPORLAMA ---
elif menu == "📊 Öğrenci Karnesi & Rapor":
    st.header("Öğrenci Gelişim Takip Ekranı")
    
    df = veri_yukle()
    
    if len(df) > 0:
        # Filtreleme Alanı
        filtre_ogrenci = st.selectbox("Raporlanacak Öğrenciyi Seçin", df["Öğrenci"].unique())
        
        # Sadece o öğrenciye ait verileri getir
        ogrenci_verisi = df[df["Öğrenci"] == filtre_ogrenci]
        
        st.info(f"📌 **{filtre_ogrenci}** isimli öğrenci için toplam **{len(ogrenci_verisi)}** ders kaydı bulundu.")
        
        # Tabloyu Göster
        st.dataframe(ogrenci_verisi.sort_values(by="Tarih", ascending=False), use_container_width=True)
        
        # Excel İndirme Butonu
        csv = ogrenci_verisi.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Bu Raporu Excel (CSV) Olarak İndir",
            data=csv,
            file_name=f'{filtre_ogrenci}_gelisim_raporu.csv',
            mime='text/csv',
        )
        
        # Basit Grafik (Performans Dağılımı)
        st.subheader("Performans Dağılımı")
        st.bar_chart(ogrenci_verisi["Performans"].value_counts())
        
    else:
        st.info("Henüz sisteme girilmiş bir veri yok. 'Ders Girişi' menüsünden ilk kaydı yapabilirsiniz.")

# --- 3. MODÜL: AYARLAR ---
elif menu == "⚙️ Ayarlar":
    st.header("Sistem Bilgisi")
    st.markdown("""
    Bu sistem **Akademi Disleksi** için özel olarak hazırlanmıştır.
    
    - **Veri Kaynağı:** `akademi_veri.csv` dosyası (Bu dosya programın olduğu klasördedir).
    - **Yedekleme:** CSV dosyasını haftalık olarak USB belleğe veya Drive'a yedeklemeniz önerilir.
    - **Geliştirme:** Bu açık kaynak kodlu bir yapıdır, ileride grafikler ve veli girişi eklenebilir.
    """)
