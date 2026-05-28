from mutagen.flac import FLAC
from pathlib import Path
import os
import re

AUDIO_FOLDER = "audio - Copy"

def sanitize_filename(name):
    # Remove invalid filename characters
    return re.sub(r'[<>:"/\\|?*]', '', name)

for root, dirs, files in os.walk(AUDIO_FOLDER):
    for file in files:
        if file.lower().endswith(".flac"):
            file_path = Path(root) / file

            try:
                audio = FLAC(file_path)

                # Get title
                title = audio.get("title", ["Unknown Title"])[0]

                # Get contributing artists
                artists = (
                    audio.get("artist")
                    or audio.get("albumartist")
                    or ["Unknown Artist"]
                )

                artist_text = ", ".join(artists)

                # Build new filename
                new_name = f"{title} - {artist_text}.flac"
                new_name = sanitize_filename(new_name)

                new_path = file_path.with_name(new_name)

                # Avoid overwriting existing files
                counter = 1
                while new_path.exists():
                    new_name = f"{title} - {artist_text} ({counter}).flac"
                    new_name = sanitize_filename(new_name)
                    new_path = file_path.with_name(new_name)
                    counter += 1

                file_path.rename(new_path)

                print(f"Renamed:")
                print(f"  {file_path.name}")
                print(f"  -> {new_path.name}")

            except Exception as e:
                print(f"Failed: {file_path}")
                print(f"Reason: {e}")