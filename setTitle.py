import os
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

folder = "songs"

for filename in os.listdir(folder):
    if filename.lower().endswith(".mp3"):
        filepath = os.path.join(folder, filename)

        # filename without extension
        title = os.path.splitext(filename)[0]

        try:
            audio = MP3(filepath, ID3=EasyID3)
        except Exception:
            audio = MP3(filepath)
            audio.add_tags()

        audio["title"] = title
        audio.save()

        print(f"Updated: {filename} -> Title: {title}")