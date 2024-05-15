import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import openai
import requests

openai.api_key = "sk-proj-BCV7li7lopfwtP6mZzoQT3BlbkFJvnFfl2loH52M0vEOy9rq"
# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Function to recognize speech and translate to text
def translate_speech_to_text():
    with sr.Microphone() as source:
        st.write("Say something in Arabic...")
        audio = recognizer.listen(source)

    try:
        st.write("Translating...")
        text = recognizer.recognize_google(audio, language='ar')
        return text
    except sr.UnknownValueError:
        st.write("Could not understand audio")
        return ""
    except sr.RequestError as e:
        st.write(f"Could not request results; {e}")
        return ""

# Function to translate text to English
def translate_text_to_english(text):
    response = openai.ChatCompletion.create(  # Using the correct method to create a chat completion
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "Translate next sentence in English. The output formate should be string."},
            {"role": "user", "content": text}
        ]
    )
    
    return response['choices'][0]['message']['content']

# Streamlit UI
st.title("Arabic to English Speech Translator")

# Initialize session state dictionary
if 'arabic_text' not in st.session_state:
    st.session_state['arabic_text'] = ""

if st.button("Recording Arabic"):
    st.session_state['arabic_text'] = translate_speech_to_text()
    st.write(f"Arabic Text: {st.session_state['arabic_text']}")
    st.write("Click 'Translate' to translate to English.")

if st.button("Translate"):
    if st.session_state['arabic_text']:
        st.session_state.english_text = translate_text_to_english(st.session_state['arabic_text'])
        st.write({st.session_state.english_text})
        st.write("Click 'Speak Translation' to hear the translation.")
    else:
        st.write("Please record Arabic speech first.")

if st.button("Speak Translation"):
    if st.session_state.english_text:
        tts = gTTS(text=st.session_state.english_text, lang='en')
        tts.save("translation.mp3")
        os.system("start translation.mp3")
    else:
        st.write("Please translate the text first.")

