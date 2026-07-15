import json

# File names
VOCALS_FILE = "musicVocals.json"
VOCALS_JP_FILE = "musicVocals-jp.json"

# Load JSON files
with open(VOCALS_FILE, "r", encoding="utf-8") as f:
    vocals = json.load(f)

with open(VOCALS_JP_FILE, "r", encoding="utf-8") as f:
    vocals_jp = json.load(f)

# Get all existing IDs from musicVocals.json
existing_ids = {item["id"] for item in vocals}

# Add items from musicVocals-jp.json if ID does not exist
added_count = 0

for item in vocals_jp:
    if item["id"] not in existing_ids:
        vocals.append(item)
        existing_ids.add(item["id"])
        added_count += 1

# Save updated musicVocals.json
with open(VOCALS_FILE, "w", encoding="utf-8") as f:
    json.dump(vocals, f, ensure_ascii=False, indent=2)

print(f"Added {added_count} new items to {VOCALS_FILE}")