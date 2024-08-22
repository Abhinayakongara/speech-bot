import tkinter as tk
from tkinter import scrolledtext
import threading
import cv2
import speech_recognition as sr
import pyttsx3

# Step 1: Speech Recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"User said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not get that.")
            return "Sorry, I did not get that."
        except sr.RequestError:
            print("Could not request results from the speech recognition service.")
            return "Service error. Please try again."

# Step 2: Mock Response Generation
def generate_response_mock(prompt):
    return "This is a mock response to your input: " + prompt

# Step 3: Text-to-Speech
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Step 4: Webcam Capture
def capture_webcam():
    cap = cv2.VideoCapture(0)  # Open the default webcam
    if not cap.isOpened():
        print("Error: Webcam not found or not accessible.")
        return
    print("Webcam is working. Press 'q' to quit.")
    try:
        while True:
            ret, frame = cap.read()  # Capture frame-by-frame
            if not ret:
                print("Error: Failed to capture image.")
                break
            cv2.imshow('Webcam Test', frame)  # Display the frame
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
                break
    except KeyboardInterrupt:
        print("Process interrupted by user.")
    finally:
        cap.release()  # Release the capture
        cv2.destroyAllWindows()  # Close all OpenCV windows

# Step 5: Tkinter GUI Interface
def start_listening():
    threading.Thread(target=main, daemon=True).start()

def update_text(text_widget, text):
    text_widget.config(state=tk.NORMAL)
    text_widget.insert(tk.END, text + "\n")
    text_widget.config(state=tk.DISABLED)

def main():
    user_input = recognize_speech()
    if user_input:
        response = generate_response_mock(user_input)
        update_text(chat_display, f"User: {user_input}")
        update_text(chat_display, f"Bot: {response}")
        speak_text(response)

# Initialize Tkinter root window
root = tk.Tk()
root.title("Speech-to-Speech LLM Bot")

# Chat display area
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Listen button
listen_button = tk.Button(root, text="Start Listening", command=start_listening)
listen_button.pack(pady=10)

# Webcam button
capture_button = tk.Button(root, text="Open Webcam", command=capture_webcam)
capture_button.pack(pady=10)

# Set window size
root.geometry("500x400")
root.mainloop()