import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
from pydub import AudioSegment
from pydub.playback import play

# Custom CSS to style the app
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌐 Arabic to English Voice Translator")

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`."""
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    try:
        response["transcription"] = recognizer.recognize_google(audio, language="ar-SA")
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

def translate_text(text, src='ar', dest='en'):
    """Translate text from source language to destination language."""
    translator = Translator()
    translation = translator.translate(text, src=src, dest=dest)
    return translation.text

def text_to_speech(text, lang='en'):
    """Convert text to speech."""
    tts = gTTS(text=text, lang=lang)
    tts.save("translated_audio.mp3")

    base_dir = os.path.dirname(__file__)
    audio_file_path = os.path.join(base_dir, "translated_audio.mp3")

    return audio_file_path

recognizer = sr.Recognizer()
microphone = sr.Microphone()

with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("👉 Press button and Speak"):
            message_placeholder = st.empty()
            message_placeholder.info("Speak now...")
            with st.spinner('Processing...'):
                speech = recognize_speech_from_mic(recognizer, microphone)

            if speech["transcription"]:
                message_placeholder.empty()
                st.success("Transcription: " + speech["transcription"])
                translation = translate_text(speech["transcription"])
                st.success("Translation: " + translation)
                
                audio_file = text_to_speech(translation)
                st.audio(audio_file, format="audio/mp3", loop=False)
                os.remove(audio_file)
            else:
                message_placeholder.empty()
                st.error(speech["error"])
