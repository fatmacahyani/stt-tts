from openai import OpenAI
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)
# systemprompt = "You are service robot. Autonomous assistant designed to enhance the experience of students, staff, and visitors at ITS campus"

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak please...")
        try:
            # audio = recognizer.listen(source)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)  # Timeout untuk idle
            text = recognizer.recognize_google(audio, language="id-ID")  # Bahasa Indonesia (belum bisa)
            print(f"You Say : {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, Voice cannot be recognized")
            return None
        except sr.WaitTimeoutError:
            print("Idle... No voice detected.")
            return None
        except sr.RequestError:
            print("There is an error with the service.")
            return None

def text_to_speech(text):
    engine = pyttsx3.init()

    # Set parameters for speech
    engine.setProperty("rate", 50)  # Speed of speech
    engine.setProperty("volume", 0.8)  # Volume (0.0 to 1.0)
    
    engine.say(text)
    engine.runAndWait()

def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            # voice="nova",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        system_response = response.choices[0].message.content
        return system_response
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, error in generating response."


def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":

    while True:
        # Langkah 1: STT
        user_input = speech_to_text()

        if user_input:
            # Langkah 2: Respons pakai GPT 
            system_response = generate_response(user_input)
            print(f"Respons: {system_response}")

            # Langkah 3: TTS
            text_to_speech(system_response)
