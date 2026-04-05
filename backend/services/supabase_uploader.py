import os
import uuid
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Configuration from env variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Warning: Supabase URL or Key not set. Direct local file serving will be used.")

# Initialize the Supabase Client
def get_supabase_client():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Error initializing Supabase client: {e}")
        return None

def upload_file(local_file_path, bucket_name="stories"):
    """
    Uploads a local file to a Supabase storage bucket and returns the public URL.
    """
    supabase = get_supabase_client()
    if not supabase:
        print("Using local file serving.")
        return local_file_path # Or some local URL if needed

    try:
        filename = os.path.basename(local_file_path)
        unique_filename = f"{uuid.uuid4().hex[:12]}_{filename}"
        
        # Open and upload file
        with open(local_file_path, 'rb') as f:
            res = supabase.storage.from_(bucket_name).upload(unique_filename, f)
            
            if hasattr(res, 'error') and res.error:
                print(f"Error uploading to Supabase: {res.error}")
                return local_file_path
            
            # Get Public URL
            public_url = supabase.storage.from_(bucket_name).get_public_url(unique_filename)
            print(f"Uploaded {local_file_path} to {public_url}")
            return public_url
            
    except Exception as e:
        print(f"Critical error during Supabase upload: {e}")
        return local_file_path # Fallback to local path

def upload_story_assets(audio_path, video_path):
    """
    Uploads both audio and video assets and returns their public URLs.
    """
    print("Uploading assets to Supabase storage...")
    audio_url = upload_file(audio_path)
    video_url = upload_file(video_path)
    
    return {
        "audio_url": audio_url,
        "video_url": video_url
    }
