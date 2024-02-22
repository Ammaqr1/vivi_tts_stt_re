import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
import pygame

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI GPT-3 API key
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Initialize pygame for audio playback
pygame.init()

def play_tts_audio(voice, model, input_text):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=input_text
    )

    # Save the generated speech to a file
    with open(speech_file_path, "wb") as f:
        f.write(response.content)

    # Load the audio file using pygame.mixer.Sound
    sound = pygame.mixer.Sound(str(speech_file_path))

    # Play the audio
    channel = sound.play()

    while True:
        user_input = input("Enter 1 to play, 2 to stop, 3 to repeat, or 0 to exit: ")

        if user_input == '1':
            channel.unpause()
        elif user_input == '2':
            channel.pause()
        elif user_input == '3':
            sound.stop()
            channel = sound.play()
        elif user_input == '0':
            break

    # Cleanup
    pygame.quit()

# Example usage:
voice_options = {"1": "nova", "2": "echo", "3": "fable", "4": "onyx", "5": "shimmer"}
model_options = {"1": "tts-1", "2": "tts-1-hd"}

print("Select Voice:")
for key, value in voice_options.items():
    print(f"{key}: {value}")

selected_voice_key = input("Enter the number corresponding to the desired voice: ")
selected_voice = voice_options.get(selected_voice_key)

print("Select Model:")
for key, value in model_options.items():
    print(f"{key}: {value}")

selected_model_key = input("Enter the number corresponding to the desired model: ")
selected_model = model_options.get(selected_model_key)

input_text = input("type something to say : ")

if selected_voice and selected_model:
    play_tts_audio(selected_voice, selected_model, input_text)
else:
    print("Invalid voice or model selected.")
