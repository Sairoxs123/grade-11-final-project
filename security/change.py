from cs50 import SQL
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import speech_recognition as sr
from time import sleep
import os

def record_audio(file_path, duration=5, sample_rate=44100):
    print("Recording audio...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype=np.int16)
    sd.wait()

    # Save the audio data to a WAV file
    write(file_path, sample_rate, audio_data)

def reconginse(audio_file1):
    db = SQL("mysql://root:@localhost:3306/final")
    # Extract speech from audio files
    r = sr.Recognizer()
    with sr.AudioFile(audio_file1) as source:
        audio1 = r.record(source)

    # Convert audio to text
    try:
        text1 = r.recognize_google(audio1)

        # Compare text transcripts
        res = db.execute("SELECT * FROM users WHERE special = (?)", text1)

        if len(res) > 0:
            return False

        else:
            return str(text1)

    except:
        return False


def change():
    db = SQL("mysql://root:@localhost:3306/final")
    name = input("Enter your name: ")
    password = input("Enter a password: ")

    results = db.execute("SELECT * FROM users WHERE name = (?)", name)

    if len(results) < 0:
        print("\nUser doesn't exist.\n")
    else:
        print("Voice recording will start in 5 seconds.")
        sleep(5)
        audio_file_path = str(name + ".wav")
        record_audio(audio_file_path)
        phrase = reconginse(audio_file_path)
        if phrase != False:
            db.execute("INSERT users special = (?) WHERE name = (?)", phrase, name)
            print("\nYou have changed your phrase successfully.\n")

        else:
            print("Special phrase is already being used by someone else.")
            os.remove(audio_file_path)
