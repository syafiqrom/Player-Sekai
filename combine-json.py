import json

# File names
MUSICS_FILE = "musicVocals.json"
MUSICS_JP_FILE = "musicVocals-jp.json"

# Load JSON files
with open(MUSICS_FILE, "r", encoding="utf-8") as f:
    musics = json.load(f)

with open(MUSICS_JP_FILE, "r", encoding="utf-8") as f:
    musics_jp = json.load(f)

# Get all existing IDs from musics.json
existing_ids = {item["id"] for item in musics}

# Add items from musics-jp.json if ID does not exist
added_count = 0

for item in musics_jp:
    if item["id"] not in existing_ids:
        musics.append(item)
        existing_ids.add(item["id"])
        added_count += 1

# Save updated musics.json
with open(MUSICS_FILE, "w", encoding="utf-8") as f:
    json.dump(musics, f, ensure_ascii=False, indent=2)

print(f"Added {added_count} new items to {MUSICS_FILE}")