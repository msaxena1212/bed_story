import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini with the API Key from Environment Variables
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

async def generate_story_stream(data):
    """
    Asynchronous generator that streams a warm, emotionally supportive story from Gemini 1.5 Flash.
    """
    # Build prompt with extreme emotional intelligence and Parent/Child connection
    prompt = f"""
    Create a {data.get('mood', 'magical')} bedtime story for {data.get('name', 'a child')} (Age: {data.get('age', 5)}).
    Theme: {data.get('theme', 'adventure')}
    
    INSTRUCTIONS FOR MAGIC & FEELING:
    1. STORY: Use 'Secure Attachment' language. Focus on the child's safety, the warmth of their bed, and their bravery through gentle kindness. The story must feel like a "hug in words."
    2. PARENT CONNECTION: After the story, add a section starting with '---PARENT TIP---' that gives the parent a specific "heart-to-heart" cuddle prompt.
    3. SEARCH KEYWORDS: Finally, add a section starting with '---SEARCH KEYWORDS---' that lists 3-5 professional, simple English keywords for a matching high-quality stock photo (e.g., "starry night space rocket").
    
    Total Story Length: 200-300 words.
    Tone: Extremely comforting, gentle, and loving. No scary elements.
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Gemini Streaming API
        response = model.generate_content(prompt, stream=True)
        
        for chunk in response:
            if chunk.text:
                yield chunk.text
                
    except Exception as e:
        print(f"Error streaming from Gemini: {e}")
        # Warm fallback if AI fails
        yield f"---STORY---\nOnce upon a time, {data.get('name', 'Hero')} felt very safe and loved. Their blanket was warm, and their heart was happy..."
