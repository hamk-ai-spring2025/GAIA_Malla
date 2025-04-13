#8 Create a voice controlled program, which utilizes AI. E.g. 
# it could be an AI image generator which uses voice input or it could be an AI image editor which allows voice input to alter the images.
#  Or it could be a program which utilizes LLM + voice output to roast the given person or topic. 
# Or it could be a program to practice language interactively. The latter would require the use of real time voice API, which can be difficult.


import replicate
import pyaudio
import wave
import speech_recognition as sr



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
    
    print("Let's create a picture! Tell me what you want to see: \n")
    input("Press Enter to start recording...")

    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Recording complete.")
    
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
    
    print(f"Audio saved to file {OUTPUT_FILENAME}")

    return (OUTPUT_FILENAME)
#<--- RecordAudio() ends here

def transcribe_audio(audio_file):
    # This function transcribes the audio file into text using the SpeechRecognition library.

    # code written by Copilot

    recognizer = sr.Recognizer()
    try:
        # Load the audio file
        with sr.AudioFile(audio_file) as source:
            #print("Processing audio...")
            audio = recognizer.record(source)  # Record audio from the file

        # Recognize speech using Google Web Speech API
        print("...transcribing audio...")
        text = recognizer.recognize_google(audio)
        #print("Transcription complete.")
        return text
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

# <-- transcribe_audio() ends here

def generate_image(prompt_text):
    # This function generates an image using the Replicate API based on the transcribed text.
	print("Generating image you described...")   
	
	output = replicate.run(
		"black-forest-labs/flux-schnell",
		input={
			"prompt": prompt_text,
			"go_fast": True,
			"megapixels": "0.25",
			"num_outputs": 1,
			"aspect_ratio": "1:1",
			"output_format": "jpg",
			"output_quality": 80,
			"num_inference_steps": 2
		}
	)
     
	print(output)

    #save the generated images
	for i in range(len(output)):
		with open(f'output_{i}.png', 'wb') as f:
			f.write(output[i].read())
		print(f"Image saved as output_{i}.png")
    
    # show urls of the generated images
	print("\n\nURLs of the generated images:")          

	for i in range(len(output)):
		print(f"output_{i}.png: {output[i].url}")
	
# <--- generate_image() ends here    

def main():
    # record voice and save it to a file 
    audio_file = recordAudio()

    # transcribe the audio file to text
    audio_text = transcribe_audio(audio_file)
    if audio_text:
        #print(f"Transcribed Text :{audio_text}\n")
        pass
    else:
        print("Could not transcribe the audio.\n")

    print (f"\nDo you want to generate an image of {audio_text}? (y/n)")
    user_input = input()
    if user_input == "y" or user_input == "Y":
        generate_image(audio_text)
    else:
        print("Image generation skipped.")
        exit(0)

    
    
if __name__ == "__main__":
    main()