import os
import platform
from gtts import gTTS
import elevenlabs
#from pydub import AudioSegment
#from pydub.playback import play

# Load ElevenLabs API key (ensure it's set in your environment variables)
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Step1: Text-to-Speech using gTTS
def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)
   # play_audio(output_filepath)

# Step2: Text-to-Speech using ElevenLabs
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client = elevenlabs.ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(text=input_text, voice="Aria", output_format="mp3_22050_32", model="eleven_turbo_v2")
    elevenlabs.save(audio, output_filepath)
   # play_audio(output_filepath)

# Play audio using Pydub
'''def play_audio(filepath):
    try:
        # Load the MP3 file using Pydub
        audio = AudioSegment.from_mp3(filepath)
        # Play the audio
        play(audio)
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")'''

# Test the functions
input_text = "Hi, this is AI Doctor!"
output_filepath_gtts = "gtts_output.mp3"
output_filepath_elevenlabs = "elevenlabs_output.mp3"

# Uncomment the method you want to test
text_to_speech_with_gtts(input_text, output_filepath_gtts)
# text_to_speech_with_elevenlabs(input_text, output_filepath_elevenlabs)
