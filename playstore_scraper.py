import os
import requests
import time
from google_play_scraper import search
from apksearch import APKPure

# --- Configuration ---
DOWNLOAD_FOLDER = "downloaded_apks"
GENRE_SEARCH = 'free games'
LIMIT = 10

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def download_file(url, title, app_id):
    clean_title = "".join([c for c in title if c.isalnum() or c in (' ', '_')]).strip()
    file_path = os.path.join(DOWNLOAD_FOLDER, f"{clean_title}.apk")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    print(f"   [*] Downloading {title}...")
    try:
        # We use a stream to handle large game files safely
        with requests.get(url, headers=headers, stream=True, timeout=30) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"   [✓] Saved to {file_path}")
    except Exception as e:
        print(f"   [X] Download failed for {title}: {e}")

# 1. Get apps from Play Store
results = search(GENRE_SEARCH, lang="en", country="us", n_hits=LIMIT)

for item in results:
    app_id = item['appId']
    title = item['title']
    print(f"\nProcessing: {title} ({app_id})")

    # 2. Try to find a link using APKPure mirror via apksearch
    try:
        searcher = APKPure(app_id)
        res = searcher.search_apk()
        
        if res:
            _, download_link = res
            download_file(download_link, title, app_id)
        else:
            print(f"   [X] No download link found on APKPure for {app_id}")
            
    except Exception as e:
        print(f"   [X] Search error: {e}")
    
    time.sleep(2) # Prevent being blocked