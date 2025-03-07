from openai import OpenAI
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import os

# Initialize the OpenAI client
client = OpenAI(api_key="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")

# Function to record audio from microphone
def record_audio(duration=5, sample_rate=44100):
    print("Recording...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    print("Recording finished.")
    write("output.wav", sample_rate, audio)  # Save as WAV file
    return "output.wav"

# Function to transcribe audio to text using OpenAI Whisper
def speech_to_text(audio_file):
    with open(audio_file, "rb") as file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=file
        )
    return transcript.text

# Function to generate text-to-speech using OpenAI TTS API
def text_to_speech(text, output_file="response.mp3"):
    response = client.audio.speech.create(
        model="tts-1",  # Use the TTS model
        voice="alloy",  # Choose from: alloy, echo, fable, onyx, shimmer, nova
        input=text
    )
    response.stream_to_file(output_file)  # Save the audio file
    print(f"Audio saved as {output_file}")

    # Play the audio file (platform-dependent)
    if os.name == "nt":  # Windows
        os.system(f"start {output_file}")
    elif os.name == "posix":  # macOS or Linux
        os.system(f"afplay {output_file}")  # macOS
        # For Linux, use: os.system(f"mpg321 {output_file}")

# Main function
def main():
    # Step 1: Record audio from microphone
    audio_file = record_audio(duration=5)  # Record for 5 seconds

    # Step 2: Convert speech to text
    user_input = speech_to_text(audio_file)
    print(f"You said: {user_input}")

    # Step 3: Generate a response using OpenAI GPT (optional)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    assistant_response = response.choices[0].message.content
    print(f"Assistant: {assistant_response}")

    # Step 4: Convert the response to speech using OpenAI TTS
    text_to_speech(assistant_response)

if __name__ == "__main__":
    main()