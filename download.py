import json
import requests
import os
import re
import time

BASE = "https://storage.sekai.best/sekai-jp-assets/music/long"

# load files
with open("output.json", "r", encoding="utf-8") as f:
    bundles = json.load(f)

with open("musicVocals.json", "r", encoding="utf-8") as f:
    vocals = json.load(f)

with open("musics.json", "r", encoding="utf-8") as f:
    musics = json.load(f)

with open("gameCharacters.json", "r", encoding="utf-8") as f:
    characters = json.load(f)

with open("outsideCharacters.json", "r", encoding="utf-8") as f:
    outside_chars = json.load(f)

# build lookup maps
music_map = {m["id"]: m["title"] for m in musics}
char_map = {c["id"]: c["givenNameEnglish"] for c in characters}
outside_map = {c["id"]: c["name"] for c in outside_chars}
vocal_map = {v["assetbundleName"]: v for v in vocals}

os.makedirs("songs", exist_ok=True)

def clean(name):
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

def format_names(names):
    if len(names) == 1:
        return names[0]
    elif len(names) == 2:
        return f"{names[0]} & {names[1]}"
    else:
        return f"{', '.join(names[:-1])} & {names[-1]}"

missing = []
errors = []

for bundle in bundles:
    url = f"{BASE}/{bundle}/{bundle}.mp3"

    vocal = vocal_map.get(bundle)
    if not vocal:
        missing.append((bundle, "NO_VOCAL_DATA"))
        continue

    music_id = vocal["musicId"]
    title = music_map.get(music_id, "unknown")

    # get character names
    names = []

    for c in vocal.get("characters", []):
        cid = c["characterId"]
        ctype = c["characterType"]

        if ctype == "game_character":
            name = char_map.get(cid, f"id{cid}")
        elif ctype == "outside_character":
            name = outside_map.get(cid, f"id{cid}")
        else:
            name = f"id{cid}"

        # normalize casing
        name = name.lower().capitalize()
        names.append(name)

    name_part = format_names(names) if names else "unknown"

    filename = clean(f"{title} - {name_part}.mp3")
    path = f"songs/{filename}"

    try:
        r = requests.get(url, timeout=10)

        if r.status_code == 200:
            with open(path, "wb") as f:
                f.write(r.content)
            print("OK:", filename)
        else:
            missing.append((bundle, title))

    except Exception:
        errors.append((bundle, title))

    time.sleep(0.3)

# save logs
with open("missing.txt", "w", encoding="utf-8") as f:
    for b, t in missing:
        f.write(f"{b} - {t}\n")

with open("errors.txt", "w", encoding="utf-8") as f:
    for b, t in errors:
        f.write(f"{b} - {t}\n")

print("Done")