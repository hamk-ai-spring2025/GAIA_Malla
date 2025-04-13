#7. Create a interpreter program. Record voice. 
# Use speech-to-text transcribe the speech input. Then translate the transcribed text into another language. 
# Finally use text-to-speech to generate speech from the translated transcript. 
# For example user could speak in English language input and then have it transcribed into English text. 
# Use AI to translate the English into another language like French 
# and then use text-so-speech and play that audio to speak out loud. What is the delay?


import pyaudio
import wave
import speech_recognition as sr
# import pyttsx3
# from googletrans import Translator
import os
# import uuid
from elevenlabs import ElevenLabs
#from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from playsound import playsound
from openai import OpenAI

# Note: The googletrans library may require a specific version to work correctly.
# pip install googletrans==4.0.0-rc1


def recordAudio():
    # This program records audio from the microphone and saves it to a WAV file.
    # The pyaudio library is used for audio recording, and the wave library is used for file handling.

    # code written by Copilot
    
    # Defining the settings
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5
    OUTPUT_FILENAME = "audio_recording.wav"
    
    # Starting pyaudio
    audio = pyaudio.PyAudio()
    
    # Starging the stream
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    
    print("Recording audio...")
    
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("...recording complete.")
    
    # Stop and close the stream
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    # Saving the file 
    wavefile = wave.open(OUTPUT_FILENAME, 'wb')
    wavefile.setnchannels(CHANNELS)
    wavefile.setsampwidth(audio.get_sample_size(FORMAT))
    wavefile.setframerate(RATE)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()
    
    print(f"Audio saved to file: {OUTPUT_FILENAME}")

    return (OUTPUT_FILENAME)
#<--- RecordAudio() ends here

def transcribe_audio(audio_file):
    # This function transcribes the audio file into text using the SpeechRecognition library.

    # code written by Copilot

    recognizer = sr.Recognizer()
    try:
        # Load the audio file
        with sr.AudioFile(audio_file) as source:
            print("Processing audio...")
            audio = recognizer.record(source)  # Record audio from the file

        # Recognize speech using Google Web Speech API
        print("...transcribing audio...")
        text = recognizer.recognize_google(audio)
        print("...transcription complete.")
        return text
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

# <-- transcribe_audio() ends here


def translateText(text_to_translate): 
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="gemma-3-12b-it")

    message = [
        {"role": "system", "content": "Translate text from english to deutch. Don't use preamble."}, # This is system prompt, Ai's role in this play
    ]

    model = "gemma-3-12b-it"  # LLM, remmber to start server in LM Studio first !!


    message.append({"role": "user", "content": text_to_translate})

    completion = client.chat.completions.create(
        model=model,
        messages=message,
        temperature=0.1,
        stream=False,
        top_p=1,
        presence_penalty=1.0,
        frequency_penalty=1.0,
    )

    tranlated_text=completion.choices[0].message.content
    return tranlated_text



    # PLAN B 
    # googletrans doesn't cooperate with the ElevenLabs API.

    # This function translates the given text into another language using the googletrans library.
    # code written by Copilot

    # translator = Translator()
    
    # src_language = "en"  
    # dest_language= "de"
    
    # try:
    #    translated = translator.translate(text_to_translate, src=src_language, dest=dest_language)
    #    return translated.text
    # except Exception as e:
    #    return f"An error occurred: {e}"

# <-- translateText() ends here


def text_to_speech(text):
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_TOKEN")
    
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)        
    response = client.text_to_speech.convert(
	voice_id="QtXsTvuI72CiSlfxczvg", # Leo liest
	output_format="mp3_44100_128",
	text=text,
	model_id="eleven_multilingual_v2"
    )

    # outputformat - MP3: The file format,  44100: The sampling rate, 44.1 kHz, the standard for CD-quality audio.
    # 128: kilobits per second (kbps)

    # play the audio
    temp_audio_file = "temp_audio.mp3"
    with open(temp_audio_file, "wb") as temp_file:
        for chunk in response:
            if chunk:
                temp_file.write(chunk)
    playsound(temp_audio_file)
    # os.remove(temp_audio_file)

    # Generating a unique file name for the output MP3 file
    # save_file_path = f"{uuid.uuid4()}.mp3"

    # Writing the audio to a file
    # with open(save_file_path, "wb") as f:
    #     for chunk in response:
    #         if chunk:
    #             f.write(chunk)

    # print(f"{save_file_path}: A new audio file was saved successfully!")

    # Return the path of the saved audio file
    # return save_file_path

# <-- text_to_speech ends here


# --- PLAN B STATRS HERE --------    
    # This function converts the given text to speech using the pyttsx3 library.
    # code written by Copilot
    
##    engine = pyttsx3.init()  # Initialize the text-to-speech engine
##    engine.setProperty('rate', 150)  # Adjust the speech rate
##    engine.setProperty('volume', 1.0)  # Set the volume (0.0 to 1.0)

    # Get available voices and set a voice
##    voices = engine.getProperty('voices')
##    engine.setProperty('voice', voices[0].id)  # Change index for different voices (e.g., voices[1].id)

    # Speak the text
##    engine.say(text)
##    engine.runAndWait() # Blocks while processing all currently queued commands. Invokes callbacks for engine notifications appropriately. Returns when all commands queued before this call are emptied from the queue.

# <-- text_to_speech PLAN B ends here


def main():   
    audio_file = ""
    audio_text = ""
    translated_text = ""

    print("=========================================")
    print ("Welcome to the Voice Interpreter Program!")
    print("English to Deutch Translator")
    print("=========================================")

    print ("Record voice, hit enter to start recording")
    input()
    audio_file = recordAudio()
    print ("\n")

    # Transcribe the audio file into text
    audio_text = transcribe_audio(audio_file)
    if audio_text:
        #print(f"Transcribed Text :{audio_text}\n")
        pass
    else:
        print("Could not transcribe the audio.\n")

    # translate the transcribed text into another language
    translated_text = translateText(audio_text)    

    print ("\n")
    print (audio_text)
    print (" is translated as ")
    print (translated_text)
    print ("\n")

    go_on = input("Do you want to hear the translated text? (y/n): ")
    if go_on.lower() == "y":

        # text-to-speech: generates speech from the translated transcript
        text_to_speech(translated_text)
        print("\n")

    print ("Thank you for using the Voice Interpreter Program!")
    print("=========================================")

if __name__ == "__main__":
    main()


    