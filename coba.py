import whisper
import openai
import speech_recognition as sr
from dotenv import load_dotenv
from gtts import gTTS
import os

# OpenAI API Key
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is None:
    raise ValueError("Please set the OPENAI_API_KEY environment variable")

openai.api_key = openai_api_key

# Load Whisper Model
whisper_model = whisper.load_model("medium")  # Anda dapat memilih model seperti "base", "small", "medium", atau "large"

def record_audio():
    """
    Merekam suara dari mikrofon langsung tanpa menyimpan file audio ke disk.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Silakan bicara...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
            print("Rekaman selesai.")
            return audio
        except sr.WaitTimeoutError:
            print("Tidak ada suara terdeteksi.")
            return None

def speech_to_text_with_whisper(audio):
    """
    Konversi audio dari mikrofon langsung ke teks menggunakan Whisper.
    """
    try:
        # Simpan audio sementara ke file WAV
        with open("temp_audio.wav", "wb") as f:
            f.write(audio.get_wav_data())

        # Gunakan Whisper untuk transkripsi
        result = whisper_model.transcribe("temp_audio.wav", language="id")
        print(f"Teks hasil STT (Whisper): {result['text']}")
        return result["text"]
    except Exception as e:
        print(f"Error dalam proses STT: {e}")
        return None

def generate_response(prompt):
    """
    Gunakan OpenAI GPT untuk menghasilkan respons berdasarkan teks input.
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        system_response = response.choices[0].message.content.strip()
        print(f"Respons dari GPT: {system_response}")
        return system_response
    except Exception as e:
        print(f"Error dalam generate response: {e}")
        return "Maaf, terjadi kesalahan dalam menghasilkan respons."

def text_to_speech(text):
    """
    Konversi teks menjadi audio menggunakan gTTS dan mainkan audio.
    """
    try:
        tts = gTTS(text, lang="id")  # Bahasa Indonesia
        tts.save("output_audio.mp3")
        os.system("start output_audio.mp3")  # Windows: "start", macOS: "open", Linux: "xdg-open"
    except Exception as e:
        print(f"Error dalam TTS: {e}")

if __name__ == "__main__":
    while True:
        # Step 1: Rekam audio
        audio = record_audio()
        if not audio:
            continue

        # Step 2: Speech-to-Text menggunakan Whisper
        user_input = speech_to_text_with_whisper(audio)
        if not user_input:
            continue

        # Step 3: Generate Response menggunakan GPT
        system_response = generate_response(user_input)

        # Step 4: Text-to-Speech
        text_to_speech(system_response)
