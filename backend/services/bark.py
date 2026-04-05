from bark import preload_models, SAMPLE_RATE
from bark import generate_audio as bark_generate_audio
import scipy.io.wavfile as wavfile
import os

# Preload models to memory
print("Preloading Bark Small models for caring voice...")
try:
    preload_models(
        text_use_small=True,
        coarse_use_small=True,
        fine_use_small=True,
        codec_use_gpu=False
    )
except Exception as e:
    print(f"Warning: Failed to preload bark models. {e}")

def generate_audio(text):
    """
    Generates a caring narrator voice for the story text.
    Uses 'v2/en_speaker_9' for a soft, warm female voice.
    """
    try:
        # History prompt for a soft-spoken, gentle narrator
        speaker = "v2/en_speaker_9"
        
        # Bark performs better when text is broken into sentences
        audio_array = bark_generate_audio(text, history_prompt=speaker)
        
        file_name = "story_voice.wav"
        wavfile.write(file_name, SAMPLE_RATE, audio_array)
        return file_name
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None
