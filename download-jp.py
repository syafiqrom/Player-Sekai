import json
import os
import requests
from mutagen.flac import FLAC
from pathlib import Path

# --- Load all JSON data once upfront ---
with open("musicVocals-jp.json", "r", encoding="utf-8") as f:
    music_vocals = json.load(f)

with open("musics.json", "r", encoding="utf-8") as f:
    music_list = json.load(f)

with open("musics-jp.json", "r", encoding="utf-8") as f:
    music_list_jp = json.load(f)

with open("gameCharacters.json", "r", encoding="utf-8") as f:
    game_characters = json.load(f)

with open("outsideCharacters.json", "r", encoding="utf-8") as f:
    outside_characters = json.load(f)

# --- Build lookup dicts for O(1) access ---
music_by_id = {m["id"]: m for m in music_list}
music_by_id_jp = {m["id"]: m for m in music_list_jp}
game_char_by_id = {c["id"]: c for c in game_characters}
outside_char_by_id = {c["id"]: c for c in outside_characters}

os.makedirs("audio", exist_ok=True)
os.makedirs("jackets", exist_ok=True)

def get_character_name(character: dict) -> str:
    char_id = character["characterId"]
    char_type = character["characterType"]

    if char_type == "game_character":
        char = game_char_by_id.get(char_id)
        if not char:
            return f"Unknown ({char_type}:{char_id})"
        first = char.get("firstName", "").strip()
        given = char.get("givenName", "").strip()
        return " ".join(filter(None, [first, given])) or "Unknown"

    elif char_type == "outside_character":
        char = outside_char_by_id.get(char_id)
        if not char:
            return f"Unknown ({char_type}:{char_id})"
        return char.get("name", "Unknown").strip()

    return "Unknown"


def download_file(url: str, dest: str) -> bool:
    """Download a file from url to dest. Returns True on success."""
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        with open(dest, "wb") as f:
            f.write(r.content)
        return True
    except requests.RequestException as e:
        print(f"  [WARN] Failed to download {url}: {e}")
        # add into log-jp.txt
        with open("log-jp.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"{url}\n")
        return False


def tag_flac(path: str, title: str, artists: list[str]) -> None:
    """Write title and artist tags to a FLAC file."""
    try:
        audio = FLAC(path)
        audio["title"] = title
        audio["artist"] = artists          # Vorbis comment supports multi-value artist
        audio["albumartist"] = ", ".join(artists)
        audio.save()
    except Exception as e:
        print(f"  [WARN] Failed to tag {path}: {e}")


# --- Download loop for audio files ---
for item in music_vocals:
    music_id = item["musicId"]
    assetbundle_name = item["assetbundleName"]
    caption = item.get("caption", "")

    # Skip if music file already exists in any child folder
    if next(Path("audio").rglob(f"{assetbundle_name}.flac"), None):
        print(f"[{assetbundle_name}] File already exists, skipping download.")
        continue

    flac_url = f"https://storage.sekai.best/sekai-jp-assets/music/long/{assetbundle_name}/{assetbundle_name}.flac"

    # Resolve song title. Try EN first, then JP as fallback
    music_entry = music_by_id.get(music_id)
    if not music_entry:
        music_entry = music_by_id_jp.get(music_id)

    title = music_entry["title"] if music_entry else f"Unknown (musicId:{music_id})"

    # Resolve all character names
    characters = item.get("characters", [])
    artist_names = [get_character_name(c) for c in characters] if characters else ["Unknown"]

    print(f"[{music_id}] {title} — {', '.join(artist_names)} ({caption})")

    # Download FLAC
    flac_dest = os.path.join("audio", f"{assetbundle_name}.flac")
    if download_file(flac_url, flac_dest):
        tag_flac(flac_dest, title, artist_names)
        print(f"  ✓ FLAC saved & tagged: {flac_dest}")

# --- Download loop for jacket images ---
for item in music_list:
    music_id = item["id"]
    assetbundle_name = item["assetbundleName"]

    jacket_url = f"https://storage.sekai.best/sekai-en-assets/music/jacket/jacket_s_{assetbundle_name}/jacket_s_{assetbundle_name}.webp"
    
    # Download jacket
    jacket_dest = os.path.join("jackets", f"jacket_s_{music_id:03d}.webp")

    # Skip if jacket already exists
    if next(Path("jackets").rglob(f"{assetbundle_name}.webp"), None):
        print(f"[{assetbundle_name}] File already exists, skipping download.")
        continue

    if download_file(jacket_url, jacket_dest):
        print(f"  ✓ Jacket saved: {jacket_dest}")
    