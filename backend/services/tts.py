import edge_tts

async def generate_audio(text):
    """
    Generates high-quality speech using Edge-TTS.
    Voice: en-US-EmmaNeural (Warm, expressive female voice)
    """
    try:
        # Emma is a very warm and gentle narrator voice
        voice = "en-US-EmmaNeural"
        output_file = "story_voice.mp3"
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        return output_file
    except Exception as e:
        print(f"Error generating Edge-TTS: {e}")
        return None
