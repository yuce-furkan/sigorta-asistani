import streamlit as st
import PyPDF2
import google.generativeai as genai

st.set_page_config(page_title="Sigorta Rehberim", page_icon="🛡️")

# API Bağlantısı
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Lütfen Secrets kısmına GEMINI_API_KEY ekleyin!")
else:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

def en_uygun_modeli_bul():
    # Sistemdeki modelleri listele ve 'generateContent' destekleyen ilk Flash veya Pro modeli seç
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            # Tercih sırası: Flash 1.5, Flash 2.0, en son hangisi varsa
            if '1.5-flash' in m.name or '2.0-flash' in m.name:
                return m.name
    return 'models/gemini-1.5-flash' # Varsayılan

def poliçe_analiz_et(metin):
    model_adi = en_uygun_modeli_bul()
    model = genai.GenerativeModel(model_adi)
    
    prompt = f"""Bir uzman sigorta danışmanı gibi davran. Aşağıdaki poliçe metnini analiz et:
    1. İMM (İhtiyari Mali Mesuliyet) limitini bul ve enflasyona göre yorumla.
    2. Muafiyetleri (kesintileri) açıkla.
    3. KRİTİK: Cam koruma/kırılması teminatı var mı? Muafiyet durumu nedir?
    4. En önemli 3 teminatı basitçe listele.
    
    Poliçe Metni: {metin[:15000]}"""
    
    response = model.generate_content(prompt)
    return response.text

st.title("🛡️ Akıllı Sigorta Analisti")
st.write("Danışman: Furkan Yüce | Ankara")

uploaded_file = st.file_uploader("Poliçe PDF'ini yükle", type="pdf")

if uploaded_file:
    with st.spinner("Yapay zeka modelleri taranıyor ve analiz ediliyor..."):
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text()
            
            analiz_sonucu = poliçe_analiz_et(full_text)
            st.success(f"Analiz Başarılı!")
            st.markdown(analiz_sonucu)
            
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
            # Hata detayını teknik olarak görelim
            st.write("Teknik Detay:", str(e))
    
    st.divider()
    whatsapp_link = "https://wa.me/905550564452?text=Poliçe%20analizim%20hakkında%20bilgi%20almak%20istiyorum."
    st.link_button("Furkan Yüce'ye WhatsApp'tan Danış", whatsapp_link)
