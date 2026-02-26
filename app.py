import streamlit as st
import PyPDF2 # PDF okuma kütüphanesi

st.set_page_config(page_title="Sigorta Rehberim", page_icon="🛡️")

def pdf_metin_ayikla(file):
    pdf_reader = PyPDF2.PdfReader(file)
    metin = ""
    for page in pdf_reader.pages:
        metin += page.extract_text()
    return metin

st.title("🛡️ Sigorta Rehberim")
st.subheader("Poliçenizi yükleyin, yapay zeka analiz etsin.")

uploaded_file = st.file_uploader("Poliçe PDF'ini seçin", type="pdf")

if uploaded_file:
    # PDF'i oku
    with st.spinner("Poliçe okunuyor, lütfen bekleyin..."):
        poliçe_metni = pdf_metin_ayikla(uploaded_file)
        
    st.success("Poliçe metni başarıyla okundu!")
    
    # Şimdilik metnin ilk 500 karakterini görelim (test için)
    st.write("### Poliçe Ön İzleme (İlk 500 Karakter)")
    st.text(poliçe_metni[:500] + "...")

    # ANALİZ BUTONU
    if st.button("Poliçeyi Sadeleştir ve Analiz Et"):
        st.write("---")
        st.info("🤖 Yapay zeka analizi hazırlanıyor...")
        # Bir sonraki adımda buraya Claude API bağlanacak
        st.markdown(f"""
        ### 📊 Analiz Sonuçları (Taslak)
        * **Poliçe Uzunluğu:** {len(poliçe_metni)} karakter.
        * **Kritik Kontrol:** İMM, Muafiyet ve Teminatlar taranıyor...
        """)
