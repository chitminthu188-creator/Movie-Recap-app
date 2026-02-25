import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from io import BytesIO

st.set_page_config(page_title="Movie Recap", page_icon="🎬", layout="wide")

st.title("Movie Recap App")
st.markdown("**ရုပ်ရှင်ကို စိတ်လှုပ်ရှားစရာ မြန်မာ Recap လုပ်ပြီး အသံနားထောင်ပါ**")

api_key = st.sidebar.text_input("Google Gemini API Key", type="password")
if api_key:
    genai.configure(api_key=api_key)

transcript = st.text_area("YouTube Transcript ကူးထည့်ပါ", height=250)

if st.button("Generate Burmese Recap"):
    if not api_key:
        st.error("API Key ထည့်ပါ")
    elif not transcript:
        st.warning("Transcript ရေးပါ")
    else:
        with st.spinner("Generating..."):
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = """Rewrite the transcript into an engaging Burmese movie recap script. Use exciting, storytelling tone. Burmese language only. 450-750 words."""
            response = model.generate_content([prompt, transcript])
            recap = response.text
            st.subheader("Generated Recap")
            st.markdown(recap)

            tts = gTTS(recap, lang="my")
            buffer = BytesIO()
            tts.write_to_fp(buffer)
            buffer.seek(0)
            st.audio(buffer, format="audio/mp3")
            st.download_button("Download MP3", buffer.getvalue(), "recap.mp3")
