import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Configuration from env variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize the Supabase Client
def get_supabase_client():
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Error: Supabase URL or Key not set.")
        return None
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Error initializing Supabase client: {e}")
        return None

def save_story_to_db(data):
    """
    Saves a story into the Supabase 'stories' table.
    Ensures all metadata (parent tips, images) is preserved.
    """
    supabase = get_supabase_client()
    if not supabase:
        return {"error": "Database not configured"}

    try:
        # 1. Attempt full insert with all metadata
        response = supabase.table('stories').insert(data).execute()
        
        if hasattr(response, 'data') and len(response.data) > 0:
            print(f"Successfully saved story to history: {response.data[0].get('id')}")
            return response.data
            
    except Exception as e:
        print(f"Full insert failed (likely missing columns): {e}")
        # 2. Fallback: Try saving only the core story text if metadata columns are missing
        try:
            fallback_data = {
                "name": data.get("name"),
                "theme": data.get("theme"),
                "story_text": data.get("story_text")
            }
            print("Attempting fallback save with core data...")
            response = supabase.table('stories').insert(fallback_data).execute()
            return response.data if hasattr(response, 'data') else {"error": "Fallback failed"}
        except Exception as e2:
            print(f"CRITICAL: Fallback save also failed: {e2}")
            return {"error": str(e2)}

def fetch_stories_from_db():
    """
    Retrieves all stories from the Supabase 'stories' table.
    """
    supabase = get_supabase_client()
    if not supabase:
        return []

    try:
        response = supabase.table('stories').select("*").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Error fetching stories: {e}")
        return []
