import requests
import time
import json
import re
import os

BASE = "https://storage.sekai.best/sekai-jp-assets/music/long"
PREFIX = "se"

# load your JSON file
with open("musics.json", "r", encoding="utf-8") as f:
    music_list = json.load(f)

# create output folder
os.makedirs("se_songs", exist_ok=True)

def clean_filename(name):
    # remove invalid characters for Windows/macOS/Linux
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    return name.strip()

missing = []
errors = []

for item in music_list:
    music_id = item["id"]
    title = item.get("title", "unknown")

    padded = f"{music_id:04d}"
    base_name = f"{PREFIX}_{padded}_01"
    url = f"{BASE}/{base_name}/{base_name}.mp3"

    safe_title = clean_filename(title)
    filename = f"songs/{safe_title}.mp3"

    try:
        r = requests.get(url, timeout=10)

        if r.status_code == 200:
            with open(filename, "wb") as f:
                f.write(r.content)
            print("Downloaded:", safe_title)

        elif r.status_code == 404:
            print("Missing:", music_id, title)
            missing.append((music_id, title))

        else:
            print("Error status:", music_id, title, r.status_code)
            errors.append((music_id, title))

    except Exception:
        print("Exception:", music_id, title)
        errors.append((music_id, title))

    time.sleep(0.3)

# save logs
with open("missing.txt", "w", encoding="utf-8") as f:
    for mid, title in missing:
        f.write(f"{mid} - {title}\n")

with open("errors.txt", "w", encoding="utf-8") as f:
    for mid, title in errors:
        f.write(f"{mid} - {title}\n")

print("Done")