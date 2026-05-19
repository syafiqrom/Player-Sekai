#!/usr/bin/env python3
"""
Sort audio flac files into subfolders based on character units.

Rules:
- Only consider characters with characterType == "game_character"
- All same unit → that unit's folder
- piapro + one other unit → other unit's folder
- piapro only → piapro folder
- Multiple different non-piapro units → mix folder
- No game_character entries → skip (file left in place)

Usage: place this script next to your gameCharacters.json, musicVocals.json,
       and the audio/ folder, then run:  python sort_audio.py
"""

import json
import shutil
from pathlib import Path

AUDIO_DIR = Path("audio")
GAME_CHARACTERS_FILE = Path("gameCharacters.json")
MUSIC_VOCALS_FILE = Path("musicVocals.json")

# Load data
with open(GAME_CHARACTERS_FILE, encoding="utf-8") as f:
    characters_raw = json.load(f)

with open(MUSIC_VOCALS_FILE, encoding="utf-8") as f:
    music_vocals = json.load(f)

# Build character id → unit map
char_unit: dict[int, str] = {c["id"]: c["unit"] for c in characters_raw}


def determine_folder(units: list[str]) -> str:
    unique = set(units)
    if len(unique) == 1:
        return unique.pop()                          # all same unit
    non_piapro = unique - {"piapro"}
    if len(non_piapro) == 1:
        return non_piapro.pop()                      # piapro + one other
    return "mix"                                     # multiple non-piapro units


moved = 0
skipped_no_char = 0
skipped_no_file = 0

for vocal in music_vocals:
    asset = vocal.get("assetbundleName")
    if not asset:
        continue

    src = AUDIO_DIR / f"{asset}.flac"
    if not src.exists():
        skipped_no_file += 1
        continue

    # Collect units for game_character entries only
    units = []
    for ch in vocal.get("characters", []):
        if ch.get("characterType") == "game_character":
            cid = ch.get("characterId")
            unit = char_unit.get(cid)
            if unit:
                units.append(unit)

    if not units:
        skipped_no_char += 1
        print(f"  SKIP (no game_character): {asset}.flac")
        continue

    folder_name = determine_folder(units)
    dest_dir = AUDIO_DIR / folder_name
    dest_dir.mkdir(parents=True, exist_ok=True)

    dest = dest_dir / f"{asset}.flac"
    shutil.move(str(src), str(dest))
    print(f"  MOVE → {folder_name}/  :  {asset}.flac  (units: {sorted(set(units))})")
    moved += 1

print(f"\nDone. Moved: {moved} | No game_character: {skipped_no_char} | File not found: {skipped_no_file}")