import streamlit as st
import PyPDF2
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="Sigorta Rehberim", page_icon="🛡️")

# API Bağlantısı (Secrets'tan alıyoruz)
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Model ismini tam olarak yazıyoruz
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Bağlantı Hatası: {e}")

def poliçe_analiz_et(metin):
    prompt = f"""Bir uzman sigorta danışmanı gibi davran. Aşağıdaki poliçe metnini analiz et:
    1. İMM (İhtiyari Mali Mesuliyet) limitini bul ve enflasyona göre yorumla.
    2. Muafiyetleri (kesintileri) açıkla.
    3. KRİTİK: Cam koruma/kırılması teminatı var mı? Muafiyet durumu nedir?
    4. En önemli 3 teminatı basitçe listele.
    
    Poliçe Metni: {metin[:15000]}""" # Gemini 3 Flash çok geniş metin okuyabilir
    
    response = model.generate_content(prompt)
    return response.text

st.title("🛡️ Akıllı Sigorta Analisti")
st.write("Profesyonel Sigorta Danışmanınız Furkan Yüce Güvencesiyle")

uploaded_file = st.file_uploader("Poliçe PDF'ini yükle", type="pdf")

if uploaded_file:
    with st.spinner("Poliçe inceleniyor..."):
        # PDF Oku
        reader = PyPDF2.PdfReader(uploaded_file)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text()
            
        # Analiz Et
        try:
            analiz_sonucu = poliçe_analiz_et(full_text)
            st.success("Analiz Tamamlandı!")
            st.markdown(analiz_sonucu)
        except Exception as e:
            st.error(f"Analiz sırasında bir hata oluştu: {e}")
    
    # WhatsApp İletişim
    st.divider()
    whatsapp_link = "https://wa.me/905550564452?text=Poliçe%20analizim%20hakkında%20bilgi%20almak%20istiyorum."
    st.link_button("Furkan Yüce'ye WhatsApp'tan Danış", whatsapp_link)
