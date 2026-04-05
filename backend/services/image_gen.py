import urllib.parse
import os
import random

def generate_image(keywords, theme):
    """
    Retrieves a professional, high-quality stock photo using Unsplash or Lorem Flickr.
    This provides a polished "Storybook" look using free online libraries.
    """
    try:
        # 1. Prepare keywords (cleaned)
        # keywords might look like "---SEARCH KEYWORDS--- starry night rocket"
        clean_keywords = keywords.replace("---SEARCH KEYWORDS---", "").strip()
        
        # 2. Prefer Unsplash for high-quality professional photography
        # Unsplash "Source" alternative: using the direct image search redirect
        encoded_query = urllib.parse.quote(clean_keywords)
        
        # We'll use a curated collection of high-quality sources
        # Lorem Flickr is great for tag-based searches without keys
        image_url = f"https://loremflickr.com/1024/1024/{encoded_query},magic,fairytale/all"
        
        # Alternative: Unsplash Source Redirect (still functional for some use cases)
        # image_url = f"https://source.unsplash.com/featured/?{encoded_query}"
        
        print(f"Professional Stock Image URL: {image_url}")
        return image_url
        
    except Exception as e:
        print(f"Error selecting stock image: {e}")
        # High-quality fallback
        return f"https://loremflickr.com/1024/1024/{theme},landscape/all"
