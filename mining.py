from gtts import gTTS
import pydub


def generate_audio_code():
    # Text for TTS generation
    text = "This is the text to be inserted."

    # Generate TTS audio using gTTS
    speech = gTTS(text=text, lang='en')
    speech.save("tts_output.mp3")

    # Existing audio file path
    existing_audio = "testaudio.mp3"

    # Desired insertion point (in seconds) in the existing audio
    insertion_point = 10  # Adjust this value as needed

    # Load the TTS and existing audio with pydub
    tts_audio = pydub.AudioSegment.from_mp3("tts_output.mp3")
    existing_segment = pydub.AudioSegment.from_mp3(existing_audio)

    # Silence (optional) before and after insertion (in milliseconds)
    silence_duration = 100

    # Create silent segments for padding
    silence_before = pydub.AudioSegment.silent(duration=silence_duration)
    silence_after = pydub.AudioSegment.silent(duration=silence_duration)

    # Combine segments in the desired order
    spliced_audio = silence_before + tts_audio + silence_after + existing_segment[
                                                                 0:insertion_point * 1000] + existing_segment[
                                                                                             insertion_point * 1000:]

    # Export the spliced audio with a new filename
    spliced_audio.export("spliced_audio.mp3", format="mp3")

    print("Audio spliced successfully!")


generate_audio_code()
