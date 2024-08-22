! pip install gtts SpeechRecognition pyaudio
import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import time

# Initialize the recognizer
recognizer = sr.Recognizer()

# Initialize pygame for audio playback
pygame.mixer.init()

def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "temp.mp3"
    tts.save(filename)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    os.remove(filename)

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print("You said: " + text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not catch that.")
            return None
        except sr.RequestError:
            print("Sorry, there is a problem with the speech recognition service.")
            return None

def chatbot_response(text):
    # Simple responses based on keywords
    if 'hello' in text.lower():
        return "Hi there! How can I help you today?"
    elif 'how are you' in text.lower():
        return "I'm just a computer program, but I'm doing well. How can I assist you?"
    else:
        return "Sorry, I don't understand that."

def main():
    while True:
        text = listen()
        if text:
            response = chatbot_response(text)
            speak(response)

if _name_ == "_main_":
    main()