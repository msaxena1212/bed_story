import re

def process_scenes(story_text: str):
    # Simple split of paragraphs
    scenes = [scene.strip() for scene in story_text.split('\n\n') if scene.strip()]
    
    # Restrict to around 3-5 scenes ideally
    return scenes[:5]
