import os
import uuid
from moviepy import ImageClip, concatenate_videoclips, AudioFileClip
from services.image_gen import generate_image
from utils.scene_splitter import process_scenes

def create_video(story_text, audio_path, theme):
    """
    Creates a video by splitting the story into scenes, generating an image for each,
    applying a Ken Burns-like effect, and merging with the audio.
    """
    print(f"Creating video from story text and audio at {audio_path}")
    
    # 1. Split story into scenes
    scenes = process_scenes(story_text)
    
    # 2. Load audio to get duration
    audio = AudioFileClip(audio_path)
    audio_duration = audio.duration
    
    # Calculate duration per scene
    scene_duration = audio_duration / len(scenes)
    
    clips = []
    
    # 3. Generate images and create clips for each scene
    for scene in scenes:
        image_path = generate_image(scene, theme)
        
        if os.path.exists(image_path) and not image_path.endswith('.png') == False: # if not placeholder
             # Simple zoom effect for Ken Burns
            clip = ImageClip(image_path).set_duration(scene_duration)
            
            # Application of a simple zoom-in effect
            # We use a lambda function to change the resize factor over time
            clip = clip.resize(lambda t: 1.0 + 0.1 * (t / scene_duration))
            clip = clip.set_position('center')
            
            clips.append(clip)
        else:
            print(f"Warning: Image generation failed or returned placeholder for scene: {scene[:30]}")
            # Fallback to a color clip or just skip
            continue

    if not clips:
        print("Error: No video clips were generated.")
        return None

    # 4. Concatenate all scene clips
    final_clip = concatenate_videoclips(clips, method="compose")
    
    # 5. Set the audio
    final_clip = final_clip.set_audio(audio)
    
    # 6. Write the final video file
    output_filename = f"story_{uuid.uuid4().hex[:8]}.mp4"
    final_clip.write_videofile(output_filename, fps=24, codec="libx264", audio_codec="aac")
    
    # Clean up audio resource
    audio.close()
    
    return output_filename
