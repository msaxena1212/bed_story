import os
import re
import asyncio
import time
from google import genai
from google.genai import types
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini client
gemini_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Supabase helper (graceful if not configured) ──────────────────────────────
def get_supabase():
    try:
        from supabase import create_client
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if url and key:
            return create_client(url, key)
    except Exception:
        pass
    return None

def save_story(data: dict):
    sb = get_supabase()
    if not sb:
        return {"status": "skipped"}
    try:
        res = sb.table("stories").insert({
            "name": data.get("name"),
            "age": data.get("age"),
            "theme": data.get("theme"),
            "mood": data.get("mood"),
            "story_text": data.get("story_text"),
            "parent_tip": data.get("parent_tip"),
            "image_url": data.get("image_url"),
        }).execute()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

def fetch_stories():
    sb = get_supabase()
    if not sb:
        return []
    try:
        res = sb.table("stories").select("*").order("created_at", desc=True).execute()
        return res.data or []
    except Exception:
        return []

# ── Image helper ──────────────────────────────────────────────────────────────
def generate_image(keywords: str, theme: str) -> str:
    clean = re.sub(r'[^a-zA-Z\s]', '', keywords).strip()
    if not clean:
        clean = theme
    slug = clean.replace(" ", ",")
    return f"https://loremflickr.com/600/400/{slug}"

# ── Gemini story generator ────────────────────────────────────────────────────
async def gemini_stream(data: dict):
    prompt = f"""
Create a {data.get('mood', 'magical')} bedtime story for {data.get('name', 'a child')} (Age: {data.get('age', 5)}).
Theme: {data.get('theme', 'adventure')}

INSTRUCTIONS:
1. STORY: Use warm, comforting 'Secure Attachment' language. The story must feel like a "hug in words."
2. PARENT CONNECTION: After the story, add a section starting exactly with '---PARENT TIP---' that gives a specific cuddle prompt.
3. SEARCH KEYWORDS: Then add a section starting exactly with '---SEARCH KEYWORDS---' listing 3-5 simple English keywords for a matching stock photo (e.g., starry night space rocket).

Total Story Length: 200-300 words. Tone: Extremely comforting, gentle, and loving.
"""
    MODELS = ["gemini-2.0-flash-lite", "gemini-2.0-flash", "gemini-1.5-flash"]
    last_error = None

    for model_name in MODELS:
        try:
            response = gemini_client.models.generate_content_stream(
                model=model_name,
                contents=prompt,
            )
            for chunk in response:
                if chunk.text:
                    yield chunk.text
            return  # Success — stop trying
        except Exception as e:
            err_str = str(e)
            last_error = e
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                print(f"Rate limited on {model_name}, trying next model...")
                time.sleep(1)  # Brief pause before fallback
                continue
            else:
                print(f"Gemini error on {model_name}: {e}")
                break

    # All models failed — yield a warm fallback
    print(f"All Gemini models failed. Last error: {last_error}")
    yield f"Once upon a time, {data.get('name', 'a brave child')} felt warm, safe, and loved. They snuggled up tight and drifted off to a peaceful sleep, knowing they were truly cherished."

# ── Routes ────────────────────────────────────────────────────────────────────
@app.post("/generate-story")
async def generate(data: dict, request: Request):
    async def story_generator():
        full_text = ""
        async for chunk in gemini_stream(data):
            full_text += chunk
            yield chunk

        # Parse metadata after full stream
        story_text = full_text
        parent_tip = "Give your child a gentle hug before sleep. 💛"
        visual_keywords = data.get("theme", "adventure")

        if "---PARENT TIP---" in full_text:
            parts = full_text.split("---PARENT TIP---")
            story_text = parts[0].strip()
            rest = parts[1] if len(parts) > 1 else ""
            if "---SEARCH KEYWORDS---" in rest:
                kw_parts = rest.split("---SEARCH KEYWORDS---")
                parent_tip = kw_parts[0].strip()
                visual_keywords = kw_parts[1].strip()
            else:
                parent_tip = rest.strip()

        clean_kw = re.sub(r'[^a-zA-Z\s]', '', visual_keywords).strip() or data.get("theme", "adventure")
        image_url = generate_image(clean_kw, data.get("theme", "Adventure"))

        yield f"\n---IMAGE URL--- {image_url}"

        # Background save
        story_data = {
            "name": data.get("name"),
            "age": data.get("age"),
            "theme": data.get("theme"),
            "mood": data.get("mood"),
            "story_text": story_text,
            "parent_tip": parent_tip,
            "image_url": image_url,
        }
        asyncio.create_task(asyncio.to_thread(save_story, story_data))

    return StreamingResponse(story_generator(), media_type="text/plain")


@app.post("/save-story")
async def save_story_endpoint(data: dict):
    return save_story(data)


@app.get("/stories")
async def get_stories():
    return fetch_stories()


@app.post("/generate-audio")
async def generate_audio_endpoint(data: dict, request: Request):
    story_text = data.get("story_text")
    if not story_text:
        return {"error": "No story text provided"}

    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        return {"error": "ElevenLabs API Key not configured"}

    try:
        import httpx, base64

        # Rachel voice — warm, soothing, perfect for bedtime
        VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        }

        # Optimize voice settings for a bedtime story
        payload = {
            "text": story_text,
            "model_id": "eleven_turbo_v2_5",
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.85,
                "style": 0.3,
                "use_speaker_boost": True
            }
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            audio_bytes = response.content

        # Return as base64 data URL — works directly in HTML <audio> tag!
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
        return {"audio_url": f"data:audio/mpeg;base64,{audio_b64}"}

    except httpx.HTTPStatusError as e:
        print(f"ElevenLabs error: {e.response.status_code} {e.response.text}")
        return {"error": f"Voice generation failed: {e.response.status_code}"}
    except Exception as e:
        print(f"Audio error: {e}")
        return {"error": str(e)}
