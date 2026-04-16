# compare only "id" attribute in musics_en.json and musics_jp.json and 
# list the id that only appear in one of the file, not both.
import json

# Load files
with open("musics_en.json", "r", encoding="utf-8") as f:
    en_data = json.load(f)

with open("musics_jp.json", "r", encoding="utf-8") as f:
    jp_data = json.load(f)

# Extract id sets
en_ids = {item["id"] for item in en_data}
jp_ids = {item["id"] for item in jp_data}

# Find differences
only_in_en = en_ids - jp_ids
only_in_jp = jp_ids - en_ids

# Output
print("IDs only in musics_en.json:")
print(sorted(only_in_en))

print("\nIDs only in musics_jp.json:")
print(sorted(only_in_jp))