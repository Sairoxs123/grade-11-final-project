from cs50 import SQL
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import speech_recognition as sr
from time import sleep
from random import choice
import pydub
import os

def random():
    chars = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '_']

    special = ""

    for i in range(5):
        special += choice(chars)

    return special


def compare_voices(audio_file1, audio_file2):
    # Extract speech from audio files
    r = sr.Recognizer()
    with sr.AudioFile(audio_file1) as source:
        audio1 = r.record(source)
    with sr.AudioFile(audio_file2) as source:
        audio2 = r.record(source)

    # Convert audio to text
    try:
        text1 = r.recognize_google(audio1)
        text2 = r.recognize_google(audio2)

        # Compare text transcripts
        if text1 == text2:
            return True
        else:
            return False

    except:
        return False


def record_audio(file_path, duration=5, sample_rate=44100):
    print("Recording audio...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype=np.int16)
    sd.wait()

    # Save the audio data to a WAV file
    write(file_path, sample_rate, audio_data)


def login():
    db = SQL("mysql://root:@localhost:3306/final")

    results = db.execute("SELECT * FROM users")

    print("Voice verification will start in 5 seconds.")
    sleep(5)
    audio_file_path = str(random() + ".wav")
    record_audio(audio_file_path)

    valid = False

    for i in results:
        recorded = str(i["audio"])

        if compare_voices(recorded, audio_file_path) == True:
            print("\nDoor is unlocked.\n")
            valid = True
            break


        else:
            valid = False

    if not valid:
        print("Phrases do not match.")

    os.remove(audio_file_path)


