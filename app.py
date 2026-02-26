import streamlit as st

# Uygulama Başlığı ve Ayarları
st.set_page_config(page_title="Sigorta Rehberim", page_icon="🛡️")

st.title("🛡️ Sigorta Rehberim")
st.subheader("Poliçenizi yükleyin, karmaşadan kurtulun!")

# 1. Dosya Yükleme Alanı
uploaded_file = st.file_uploader("Poliçe PDF dosyasını buraya sürükleyin", type="pdf")

if uploaded_file is not None:
    st.success("Poliçe başarıyla yüklendi! Analiz ediliyor...")
    
    # İleride burası Yapay Zeka (Claude API) ile bağlanacak
    # Şimdilik senin istediğin o 3 kritik başlığı simüle ediyoruz
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("### 🚗 İMM Limiti")
        st.write("**Mevcut:** 10.000.000 TL")
        st.warning("⚠️ Not: Enflasyon karşısında bu limit riskli olabilir. 20M+ önerilir.")

    with col2:
        st.error("### 🔍 Muafiyetler")
        st.write("- Deprem hasarlarında %2 muafiyet.")
        st.write("- Cam kırılmasında 1 defaya mahsus muafiyetsiz değişim.")

    st.divider()
    
    st.success("### ✅ Teminatlar ve Avantajlar")
    st.markdown("""
    * **Yol Yardım:** 7/24 sınırsız çekici hizmeti.
    * **İkame Araç:** Yılda 2 kez, 15 güne kadar araç desteği.
    * **Mini Onarım:** Boyasız göçük düzeltme dahil.
    """)
    
    # Danışman Notu (Senin dokunuşun)
    st.chat_message("assistant").write("Merhaba Furkan, bu poliçe genel olarak iyi ama İMM limitini yükseltmen için bir ek zeyilname yaptırmanı öneririm.")

else:
    st.info("Lütfen analiz için bir poliçe dosyası yükleyin.")
