from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from pipeline.story_generator import generate_story, parse_scenes
from pipeline.image_generator import generate_images
from pipeline.media_processor import process_audio, process_video
from pipeline.supabase_uploader import upload_files

load_dotenv()

app = FastAPI(title="StoryMagic AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StoryRequest(BaseModel):
    name: str
    age: int
    theme: str
    mood: str
    learning: bool = True

@app.post("/generate-story")
async def create_story(req: StoryRequest):
    try:
        # Step 1: Generate Story Text & Split Scenes
        story_text = await generate_story(req.name, req.age, req.theme, req.mood, req.learning)
        scenes = parse_scenes(story_text)
        if not scenes:
            raise HTTPException(status_code=500, detail="Failed to parse scenes from story")

        # Step 2: Generate Audio (Bark)
        audio_file = await process_audio(story_text)

        # Step 3: Generate Images (Stable Diffusion)
        image_files = await generate_images(scenes)

        # Step 4: Generate Animation & Final Video (MoviePy + Ken Burns)
        final_video = await process_video(image_files, audio_file)

        # Step 5: Upload to Supabase
        urls = await upload_files(audio_file, final_video)

        return urls

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
