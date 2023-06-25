import requests
import random
import string
import os
import speech_recognition as sr
from pydub import AudioSegment

def generate_random_filename(length=10):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for _ in range(length))
    filename = f"{random_string}.mp3"
    return filename

def download_mp3(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)
    print('Sound Verification berhasil diunduh.')

url = input("Masukkan URL MP3: ")
filename = generate_random_filename()
save_path = filename
download_mp3(url, save_path)

script_directory = os.path.dirname(os.path.abspath(__file__))
audio_file_path = os.path.join(script_directory, save_path)

wav_filename = generate_random_filename()
wav_file_path = os.path.join(script_directory, f"{wav_filename}.wav")
audio = AudioSegment.from_mp3(audio_file_path)
audio.export(wav_file_path, format='wav')

recognizer = sr.Recognizer()

with sr.AudioFile(wav_file_path) as source:
    audio_data = recognizer.record(source)

try:
    transcript = recognizer.recognize_google(audio_data, language='en')
    print("Result Text:")
    print(transcript)
except sr.UnknownValueError:
    print("Speech recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

os.remove(audio_file_path)
os.remove(wav_file_path)
