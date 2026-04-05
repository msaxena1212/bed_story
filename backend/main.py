from fastapi import FastAPI, Request
from services.ollama import generate_story_stream
from services.storage import save_story_to_db, fetch_stories_from_db
from services.tts import generate_audio
from services.image_gen import generate_image
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serves generated files from the current directory
app.mount("/static", StaticFiles(directory="."), name="static")

@app.post("/generate-story")
async def generate(data: dict, request: Request):
    # Log incoming request
    print(f"Received request: {data}")
    
    async def story_generator():
        full_text = ""
        # 1. Stream the story from Ollama
        async for chunk in generate_story_stream(data):
            full_text += chunk
            yield chunk

        # 2. Extract parts for storage AFTER streaming
        story_parts = full_text.split("---PARENT TIP---")
        story_text = story_parts[0].strip()
        
        parent_tip = "Give your child a gentle hug for a sweet sleep."
        visual_keywords = data.get("theme", "Adventure")
        
        if len(story_parts) > 1:
            tip_parts = story_parts[1].split("---SEARCH KEYWORDS---")
            parent_tip = tip_parts[0].strip()
            if len(tip_parts) > 1:
                visual_keywords = tip_parts[1].strip()

        # 3. GENERATE PROFESSIONAL IMAGE URL
        # Clean keywords to remove all markdown, bolding, and non-alphanumeric noise
        import re
        clean_keywords = re.sub(r'[^a-zA-Z0-0\s]', '', visual_keywords).strip()
        # Remove common "noise" words from the AI
        clean_keywords = clean_keywords.replace("SEARCH KEYWORDS", "").replace("PARENT TIP", "").strip()
        
        image_url = generate_image(clean_keywords, data.get("theme", "Adventure"))

        # 4. YIELD METADATA AT THE END OF THE STREAM
        yield f"---IMAGE URL--- {image_url}"

        # 5. SAVE TO DB ASYNCHRONOUSLY
        story_data = {
            "name": data.get("name", "Child"),
            "age": data.get("age", 5),
            "theme": data.get("theme", "Adventure"),
            "mood": data.get("mood", "Magical"),
            "story_text": story_text,
            "parent_tip": parent_tip,
            "image_url": image_url
        }
        
        # Non-blocking save
        asyncio.create_task(async_save(story_data))

    async def async_save(story_data):
        save_res = save_story_to_db(story_data)
        print(f"Auto-save status: {save_res}")

    return StreamingResponse(story_generator(), media_type="text/plain")

@app.post("/generate-audio")
async def generate_audio_endpoint(data: dict, request: Request):
    # Log incoming request
    print(f"Generating high-quality Edge-TTS audio for story...")
    story_text = data.get("story_text")
    if not story_text:
        return {"error": "No story text provided"}
        
    # Await the async function correctly
    audio_path = await generate_audio(story_text)
    if not audio_path:
        return {"error": "Audio generation failed"}
        
    base_url = str(request.base_url).rstrip("/")
    audio_url = f"{base_url}/static/{audio_path}"
    
    return {"audio_url": audio_url}

@app.post("/save-story")
async def save_story(data: dict):
    # Log incoming request
    print(f"Saving story request: {data}")
    res = save_story_to_db(data)
    return res

@app.get("/stories")
async def get_stories():
    # Fetch stories from history
    stories = fetch_stories_from_db()
    return stories
