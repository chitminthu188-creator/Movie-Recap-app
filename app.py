import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from io import BytesIO
from youtube_transcript_api import YouTubeTranscriptApi
import re

# Page config
st.set_page_config(page_title="Movie Recap", page_icon="🎬", layout="wide")

# Sidebar
with st.sidebar:
    st.title("⚙️ ဆက်တင်များ")
    
    # Logo upload
    logo_file = st.file_uploader("Logo တင်ပါ (PNG/JPG)", type=["png", "jpg", "jpeg"])
    if logo_file:
        st.image(logo_file, width=150)
        st.session_state.logo = logo_file.getvalue()  # သိမ်းထားမယ်

    # Gemini API Key
    api_key = st.text_input("Google Gemini API Key", type="password")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            st.success("API Key ချိတ်ဆက်ပြီး", icon="✅")
        except Exception as e:
            st.error(f"API Key ချို့ယွင်းချက်: {str(e)}")

# Header with logo
col1, col2 = st.columns([1, 5])
with col1:
    if 'logo' in st.session_state:
        st.image(st.session_state.logo, width=100)
    else:
        st.markdown("🎬")
with col2:
    st.title("Movie Recap App")
    st.markdown("**ရုပ်ရှင်ကို စိတ်လှုပ်ရှားစရာ မြန်မာ Recap လုပ်ပြီး အသံနားထောင်ပါ**")

# Input tabs
tab1, tab2, tab3 = st.tabs(["📋 Paste Transcript", "🎥 YouTube URL", "📤 Video Upload"])

transcript = ""

with tab1:
    transcript = st.text_area("Transcript ကူးထည့်ပါ", height=220)

with tab2:
    yt_url = st.text_input("YouTube URL ထည့်ပါ")
    if st.button("YouTube Transcript ယူမယ်") and yt_url:
        with st.spinner("ရှာနေပါတယ်..."):
            try:
                video_id = re.search(r"(?:v=|youtu\.be/)([^&\n?#]+)", yt_url).group(1)
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['my', 'en'])
                transcript = " ".join([d['text'] for d in transcript_list])
                st.success("Transcript ရပါပြီ!")
                st.text_area("ရရှိတဲ့ Transcript", transcript, height=150)
            except Exception as e:
                st.error(f"မရပါ: {str(e)}")

with tab3:
    video_file = st.file_uploader("Video တင်ပါ (MP4, max \~100MB)", type=["mp4", "mov"])
    if video_file:
        st.info("လက်ရှိမှာ video → transcript လုပ်ဖို့ Whisper model ထည့်ထားခြင်း မရှိသေးပါ။ လိုအပ်ရင် နောက်မှ ထပ်ထည့်ပေးနိုင်ပါတယ်။")

# Use fetched transcript if available
if transcript == "" and 'transcript' in st.session_state:
    transcript = st.session_state.transcript

# Generate button
if st.button("✨ မြန်မာ Recap ထုတ်ပါ", type="primary", use_container_width=True):
    if not api_key:
        st.error("API Key ထည့်ပါ")
    elif not transcript.strip():
        st.warning("Transcript အနည်းဆုံး တစ်ကြောင်း ရေးပါ")
    else:
        with st.spinner("Gemini ရေးနေပါတယ်..."):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = """အရမ်းစိတ်လှုပ်ရှားစရာ မြန်မာ ရုပ်ရှင် recap script ရေးပါ။ စိတ်လှုပ်ရှားတဲ့ storytelling tone၊ မြန်မာစာ အပြည့်အစုံ၊ ၄၅၀-၇၅၀ စကားလုံး။"""
                response = model.generate_content(prompt + "\n\nTranscript:\n" + transcript)
                recap = response.text.strip()
                st.subheader("✨ Generated Recap")
                st.markdown(recap)

                # Audio
                tts = gTTS(recap, lang="my")
                buffer = BytesIO()
                tts.write_to_fp(buffer)
                buffer.seek(0)
                st.audio(buffer, format="audio/mp3")
                st.download_button("📥 MP3 ဒေါင်းလုဒ်", buffer.getvalue(), "recap.mp3", "audio/mpeg")

            except Exception as e:
                st.error(f"အမှားတက်သွားပါပြီ: {str(e)}")

st.caption("Made with ❤️ | Gemini + gTTS + youtube-transcript-api")
