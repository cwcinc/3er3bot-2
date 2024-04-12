from pydub import AudioSegment
from gtts import gTTS
import random


def create_tts_code(code):
    text = code

    speech = gTTS(text=text, lang='en')
    speech.save("tts_output.mp3")


def splice_audio_files(source_audio_path, splice_audio_path, splice_position_ms):
    # Load the source audio file
    source_audio = AudioSegment.from_file(source_audio_path)

    # Load the splice audio file
    splice_audio = AudioSegment.from_file(splice_audio_path)

    # Extract the portion of the source audio after the splice point
    source_audio_after_splice = source_audio[splice_position_ms:]

    # Splice the audio files
    new_audio = source_audio[:splice_position_ms] + splice_audio + source_audio_after_splice

    # Export the new audio
    output_path = "miningChallenge.mp3"  # Change this to your desired output path
    print("exporting...")
    new_audio.export(output_path, format="mp3", bitrate="16k")

    print("Audio splicing completed successfully!")


def generate_final_audio(code):
    code = " ".join(str(code))
    create_tts_code(code)
    splice_time = random.randint(1*60*1000, 40*60*1000)
    print("TTS created. Splicing audio...")
    splice_audio_files("testaudio.mp3", "tts_output.mp3", splice_time)
