import streamlit as st
import PyPDF2
from groq import Groq

st.set_page_config(page_title="Sigorta Rehberim", page_icon="🛡️")

# Groq Bağlantısı
if "GROQ_API_KEY" not in st.secrets:
    st.error("Lütfen Secrets kısmına GROQ_API_KEY ekleyin!")
else:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def poliçe_analiz_et(metin):
    # Llama 3 veya Mixtral modellerini kullanabiliriz, Llama 3.3 çok güçlüdür
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Sen uzman bir sigorta danışmanısın. Karmaşık poliçe metinlerini sadeleştirip müşteriye kritik uyarılar yaparsın."
            },
            {
                "role": "user",
                "content": f"""Aşağıdaki poliçe metnini analiz et:
                1. İMM (İhtiyari Mali Mesuliyet) limitini bul ve yorumla.
                2. Muafiyetleri (kesintileri) listele.
                3. KRİTİK: Cam koruma/kırılması teminatı var mı? Muafiyet durumu nedir?
                4. En önemli 3 teminatı listele.
                
                Poliçe Metni: {metin[:20000]}"""
            }
        ],
        temperature=0.5,
        max_tokens=1500
    )
    return completion.choices[0].message.content

st.title("🛡️ Akıllı Sigorta Analisti (Groq)")
st.write("Profesyonel Sigorta Danışmanı: Furkan Yüce")

uploaded_file = st.file_uploader("Poliçe PDF'ini yükle", type="pdf")

if uploaded_file:
    with st.spinner("Groq saniyeler içinde analiz ediyor..."):
        try:
            reader = PyPDF2.PdfReader(uploaded_file)
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text()
            
            analiz_sonucu = poliçe_analiz_et(full_text)
            st.success("Analiz Tamamlandı!")
            st.markdown(analiz_sonucu)
            
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")

    st.divider()
    whatsapp_link = "https://wa.me/905550564452?text=Poliçe%20analizim%20hakkında%20bilgi%20almak%20istiyorum."
    st.link_button("Furkan Yüce'ye WhatsApp'tan Danış", whatsapp_link)
