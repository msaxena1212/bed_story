import httpx
import json

async def generate_story_stream(data):
    """
    Asynchronous generator that streams a warm, emotionally supportive story from Llama 3.2.
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

    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "glm-5:cloud",
        "prompt": prompt,
        "stream": True
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", url, json=payload) as response:
                async for line in response.aiter_lines():
                    if line:
                        chunk = json.loads(line)
                        if "response" in chunk:
                            yield chunk["response"]
                        if chunk.get("done"):
                            break
    except Exception as e:
        print(f"Error streaming from Ollama: {e}")
        # Warm fallback
        yield f"---STORY---\nOnce upon a time, {data.get('name', 'Hero')} felt very safe and loved. Their blanket was warm, and their heart was happy..."
