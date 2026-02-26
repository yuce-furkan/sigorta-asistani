import streamlit as st
import PyPDF2
import google.generativeai as genai

st.set_page_config(page_title="Sigorta Rehberim", page_icon="🛡️")

# Gemini Bağlantısı
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('models/gemini-1.5-flash')

def poliçe_analiz_et(metin):
    # Senin "Cam Koruma" hassasiyetini içeren prompt
    prompt = f"""Bir uzman sigorta danışmanı gibi davran. Aşağıdaki poliçe metnini analiz et:
    1. İMM (İhtiyari Mali Mesuliyet) limitini bul, enflasyona göre yeterli mi yorumla.
    2. Muafiyetleri (kesintileri) açıkla.
    3. KRİTİK: Cam koruma/kırılması teminatı var mı? Muafiyet durumu nedir? (Bu konu bizim için çok önemli).
    4. En önemli 3 teminatı basitçe listele.
    
    Poliçe Metni: {metin[:8000]}""" # Gemini daha fazla karakter okuyabilir
    
    response = model.generate_content(prompt)
    return response.text

st.title("🛡️ Akıllı Sigorta Analisti (Gemini)")
uploaded_file = st.file_uploader("Poliçe PDF'ini yükle", type="pdf")

if uploaded_file:
    with st.spinner("Gemini poliçeyi inceliyor..."):
        reader = PyPDF2.PdfReader(uploaded_file)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text()
            
        analiz_sonucu = poliçe_analiz_et(full_text)
        
    st.success("Analiz Tamamlandı!")
    st.markdown(analiz_sonucu)
    
    # Senin iletişim butonun
    st.divider()
    st.write("### Sorularınız mı var?")
    whatsapp_link = "https://wa.me/905550564452?text=Poliçe%20analizim%20hakkında%20bilgi%20almak%20istiyorum."
    st.link_button("Furkan Yüce'ye WhatsApp'tan Sor", whatsapp_link)
