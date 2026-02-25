import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from io import BytesIO
import os
import tempfile

# Page config
st.set_page_config(
    page_title="Movie Recap - မြန်မာ Recap",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
with st.sidebar:
    st.title("⚙️ ဆက်တင်များ")
    api_key = st.text_input("Google Gemini API Key", type="password", help="https://aistudio.google.com/app/apikey မှ ယူပါ")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            st.success("API Key ချိတ်ဆက်ပြီး", icon="✅")
        except Exception as e:
            st.error(f"API Key ချို့ယွင်းချက်: {str(e)[:100]}...")

# Header
st.title("🎬 Movie Recap App")
st.markdown("**YouTube Transcript ကနေ စိတ်လှုပ်ရှားစရာ မြန်မာ recap နဲ့ အသံ ထုတ်ပေးတယ်**")
st.caption("Gemini 1.5 Flash + gTTS သုံးထားပါတယ်")

# Main input
transcript = st.text_area(
    "YouTube Transcript ကူးထည့်ပါ (သို့မဟုတ် ကော်ပီ ကူးထည့်ပါ)",
    height=220,
    placeholder="ရုပ်ရှင်ရဲ့ ဇာတ်လမ်း အကျဉ်းချုပ် / စကားပြော စာသားတွေ ထည့်ပါ..."
)

if st.button("✨ မြန်မာ Recap ထုတ်ပါ", type="primary", use_container_width=True):
    if not api_key:
        st.error("Sidebar မှာ Gemini API Key ထည့်ပါ")
    elif not transcript.strip():
        st.warning("Transcript အနည်းဆုံး တစ်ကြောင်း ရေးထည့်ပါ")
    else:
        with st.spinner("Gemini က စိတ်လှုပ်ရှားစရာ recap ရေးနေပါတယ်..."):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                prompt = """သင်ဟာ အရမ်းကောင်းတဲ့ ရုပ်ရှင် recap ပြုလုပ်သူ တစ်ယောက်ပါ။
အောက်ပါ transcript ကို ကြည့်ပြီး အလွန်စိတ်လှုပ်ရှားဖွယ်၊ ဆွဲဆောင်မှုရှိတဲ့ မြန်မာ ရုပ်ရှင် recap script တစ်ခု ရေးပေးပါ။

Requirements:
- စိတ်လှုပ်ရှားစရာ trailer အသံထွက် ပုံစံ (excited, dramatic, fun tone)
- အဓိက plot points တွေ ထည့်ပါ (spoiler မလွန်အောင် ဂရုစိုက်)
- မြန်မာစာ အပြည့်အစုံ သုံးပါ၊ အင်္ဂလိပ်စကား လုံးဝ မပါပါနဲ့
- အရှည် ၄၅၀-၇၅၀ စကားလုံး ဝန်းကျင်
- အသံနားထောင်ဖို့ သင့်တော်တဲ့ စကားပြော ပုံစံ

အခု စရေးပါ:"""
                
                response = model.generate_content(prompt + "\n\nTranscript:\n" + transcript)
                recap_text = response.text.strip()
                
                st.subheader("✨ Generated Burmese Movie Recap")
                st.markdown(recap_text)
                
                # Audio generation
                with st.spinner("အသံ ထုတ်နေပါတယ်..."):
                    tts = gTTS(text=recap_text, lang="my", slow=False)
                    audio_buffer = BytesIO()
                    tts.write_to_fp(audio_buffer)
                    audio_buffer.seek(0)
                    
                    st.audio(audio_buffer, format="audio/mp3")
                    
                    # Download button
                    st.download_button(
                        label="📥 MP3 ဒေါင်းလုဒ်လုပ်ပါ",
                        data=audio_buffer.getvalue(),
                        file_name="burmese_movie_recap.mp3",
                        mime="audio/mpeg"
                    )
                    
            except Exception as e:
                st.error(f"အမှားတက်သွားပါပြီ: {str(e)}")
                st.info("API Key မှန်ကန်မှု၊ internet ချိတ်ဆက်မှု စစ်ဆေးပြီး နောက်တစ်ခါ ကြိုးစားကြည့်ပါ")

st.divider()import streamlit as st
import google.generativeai as genai
from gtts import gTTS
from io import BytesIO
import os
import tempfile

# Page config
st.set_page_config(
    page_title="Movie Recap - မြန်မာ Recap",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
with st.sidebar:
    st.title("⚙️ ဆက်တင်များ")
    api_key = st.text_input("Google Gemini API Key", type="password", help="https://aistudio.google.com/app/apikey မှ ယူပါ")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            st.success("API Key ချိတ်ဆက်ပြီး", icon="✅")
        except Exception as e:
            st.error(f"API Key ချို့ယွင်းချက်: {str(e)[:100]}...")

# Header
st.title("🎬 Movie Recap App")
st.markdown("**YouTube Transcript ကနေ စိတ်လှုပ်ရှားစရာ မြန်မာ recap နဲ့ အသံ ထုတ်ပေးတယ်**")
st.caption("Gemini 1.5 Flash + gTTS သုံးထားပါတယ်")

# Main input
transcript = st.text_area(
    "YouTube Transcript ကူးထည့်ပါ (သို့မဟုတ် ကော်ပီ ကူးထည့်ပါ)",
    height=220,
    placeholder="ရုပ်ရှင်ရဲ့ ဇာတ်လမ်း အကျဉ်းချုပ် / စကားပြော စာသားတွေ ထည့်ပါ..."
)

if st.button("✨ မြန်မာ Recap ထုတ်ပါ", type="primary", use_container_width=True):
    if not api_key:
        st.error("Sidebar မှာ Gemini API Key ထည့်ပါ")
    elif not transcript.strip():
        st.warning("Transcript အနည်းဆုံး တစ်ကြောင်း ရေးထည့်ပါ")
    else:
        with st.spinner("Gemini က စိတ်လှုပ်ရှားစရာ recap ရေးနေပါတယ်..."):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                prompt = """သင်ဟာ အရမ်းကောင်းတဲ့ ရုပ်ရှင် recap ပြုလုပ်သူ တစ်ယောက်ပါ။
အောက်ပါ transcript ကို ကြည့်ပြီး အလွန်စိတ်လှုပ်ရှားဖွယ်၊ ဆွဲဆောင်မှုရှိတဲ့ မြန်မာ ရုပ်ရှင် recap script တစ်ခု ရေးပေးပါ။

Requirements:
- စိတ်လှုပ်ရှားစရာ trailer အသံထွက် ပုံစံ (excited, dramatic, fun tone)
- အဓိက plot points တွေ ထည့်ပါ (spoiler မလွန်အောင် ဂရုစိုက်)
- မြန်မာစာ အပြည့်အစုံ သုံးပါ၊ အင်္ဂလိပ်စကား လုံးဝ မပါပါနဲ့
- အရှည် ၄၅၀-၇၅၀ စကားလုံး ဝန်းကျင်
- အသံနားထောင်ဖို့ သင့်တော်တဲ့ စကားပြော ပုံစံ

အခု စရေးပါ:"""
                
                response = model.generate_content(prompt + "\n\nTranscript:\n" + transcript)
                recap_text = response.text.strip()
                
                st.subheader("✨ Generated Burmese Movie Recap")
                st.markdown(recap_text)
                
                # Audio generation
                with st.spinner("အသံ ထုတ်နေပါတယ်..."):
                    tts = gTTS(text=recap_text, lang="my", slow=False)
                    audio_buffer = BytesIO()
                    tts.write_to_fp(audio_buffer)
                    audio_buffer.seek(0)
                    
                    st.audio(audio_buffer, format="audio/mp3")
                    
                    # Download button
                    st.download_button(
                        label="📥 MP3 ဒေါင်းလုဒ်လုပ်ပါ",
                        data=audio_buffer.getvalue(),
                        file_name="burmese_movie_recap.mp3",
                        mime="audio/mpeg"
                    )
                    
            except Exception as e:
                st.error(f"အမှားတက်သွားပါပြီ: {str(e)}")
                st.info("API Key မှန်ကန်မှု၊ internet ချိတ်ဆက်မှု စစ်ဆေးပြီး နောက်တစ်ခါ ကြိုးစားကြည့်ပါ")

st.divider()
st.caption("Made with ❤️ | Gemini + gTTS | Streamlit Community Cloud")
st.caption("Made with ❤️ | Gemini + gTTS | Streamlit Community Cloud")"Add complete Streamlit app code"
