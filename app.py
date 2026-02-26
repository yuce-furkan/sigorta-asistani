import streamlit as st
import PyPDF2
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Sigorta Rehberim", page_icon="🛡️")

# API Bağlantısı
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Lütfen Streamlit Cloud ayarlarına GEMINI_API_KEY ekleyin!")
else:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def poliçe_analiz_et(metin):
    # En kararlı model ismini kullanıyoruz
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""Bir uzman sigorta danışmanı gibi davran. Aşağıdaki poliçe metnini analiz et:
    1. İMM (İhtiyari Mali Mesuliyet) limitini bul ve enflasyona göre yeterli mi yorumla.
    2. Muafiyetleri (kesintileri) açıkla.
    3. KRİTİK: Cam koruma/kırılması teminatı var mı? Muafiyet durumu nedir?
    4. En önemli 3 teminatı basitçe listele.
    
    Poliçe Metni: {metin[:15000]}"""
    
    response = model.generate_content(prompt)
    return response.text

st.title("🛡️ Akıllı Sigorta Analisti")
st.write(f"Danışman: Furkan Yüce | Bölge: Ankara")

uploaded_file = st.file_uploader("Poliçe PDF'ini yükle", type="pdf")

if uploaded_file:
    with st.spinner("Poliçe inceleniyor..."):
        try:
            # PDF Oku
            reader = PyPDF2.PdfReader(uploaded_file)
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text()
            
            # Analiz Et
            analiz_sonucu = poliçe_analiz_et(full_text)
            st.success("Analiz Tamamlandı!")
            st.markdown(analiz_sonucu)
            
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
    
    st.divider()
    whatsapp_link = "https://wa.me/905550564452?text=Poliçe%20analizim%20hakkında%20bilgi%20almak%20istiyorum."
    st.link_button("Furkan Yüce'ye WhatsApp'tan Danış", whatsapp_link)
