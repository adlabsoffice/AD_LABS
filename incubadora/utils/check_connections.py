import os
import sys
from dotenv import load_dotenv
from googleapiclient.discovery import build
from groq import Groq

# Load env from parent dir (incubadora)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir) # incubadora
sys.path.append(parent_dir)

env_path = os.path.join(parent_dir, ".env")
load_dotenv(env_path)

def check_youtube():
    # User confirmed keys are present. Trying VIDEO key which is likely the main one.
    key = os.getenv("YOUTUBE_DATA_API_KEY") or os.getenv("GOOGLE_API_KEY_VIDEO")
          
    if not key:
        print("[FAIL] No YOUTUBE_DATA_API_KEY or GOOGLE_API_KEY_VIDEO found in .env")
        return False
    
    print(f"[INFO] Testing Key: {key[:4]}...{key[-4:]}")
    
    try:
        youtube = build('youtube', 'v3', developerKey=key)
        request = youtube.videos().list(chart='mostPopular', regionCode='US', part='snippet', maxResults=1)
        response = request.execute()
        title = response['items'][0]['snippet']['title']
        # Encode to ascii to avoid console errors
        safe_title = title.encode('ascii', 'ignore').decode('ascii')
        print(f"[OK] YouTube API Connected. Top Video US: {safe_title}")
        return True
    except Exception as e:
        print(f"[FAIL] YouTube API Error: {e}")
        return False

def check_groq():
    key = os.getenv("GROQ_API_KEY")
    if not key:
        print("[FAIL] GROQ_API_KEY missing in .env")
        return False
        
    print(f"[INFO] Found GROQ_API_KEY: {key[:4]}...{key[-4:]}")

    try:
        client = Groq(api_key=key)
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": "Say OK"}],
            model="llama-3.3-70b-versatile",
        )
        print(f"[OK] Groq API Connected.")
        return True
    except Exception as e:
        print(f"[FAIL] Groq API Error: {e}")
        return False

if __name__ == "__main__":
    print(f"--- Checking Connections (Env: {env_path}) ---")
    yt = check_youtube()
    gr = check_groq()
    
    if yt and gr:
        print("\n[SUCCESS] All systems GO for Real Mode!")
    else:
        print("\n[WARNING] Some systems failed. Check .env")
