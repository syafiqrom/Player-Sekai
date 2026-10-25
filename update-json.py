import json
import requests
from pathlib import Path

FILES = [
    {
        "url": "https://sekai-world.github.io/sekai-master-db-en-diff/musics.json",
        "local": "musics-en.json"
    },
    {
        "url": "https://sekai-world.github.io/sekai-master-db-diff/musics.json",
        "local": "musics-jp.json"
    },
    {
        "url": "https://sekai-world.github.io/sekai-master-db-en-diff/musicVocals.json",
        "local": "musicVocals-en.json"
    },
    {
        "url": "https://sekai-world.github.io/sekai-master-db-diff/musicVocals.json",
        "local": "musicVocals-jp.json"
    },
    {
        "url": "https://sekai-world.github.io/sekai-master-db-en-diff/musicOriginals.json",
        "local": "musicOriginals-en.json"
    },
    {
        "url": "https://sekai-world.github.io/sekai-master-db-diff/musicOriginals.json",
        "local": "musicOriginals-jp.json"
    }
]

COMBINE_PAIRS = [
    {"en": "musics-en.json",        "jp": "musics-jp.json",        "out": "musics.json"},
    {"en": "musicVocals-en.json",   "jp": "musicVocals-jp.json",   "out": "musicVocals.json"},
    {"en": "musicOriginals-en.json","jp": "musicOriginals-jp.json", "out": "musicOriginals.json"},
]


def update_json(url, local_file) -> bool:
    print(f"\nChecking {local_file}...")

    response = requests.get(url)
    response.raise_for_status()
    online_data = response.json()

    if not Path(local_file).exists():
        with open(local_file, "w", encoding="utf-8") as f:
            json.dump(online_data, f, ensure_ascii=False, indent=2)
        print(f"Created {local_file}")
        return True

    with open(local_file, "r", encoding="utf-8") as f:
        local_data = json.load(f)

    local_ids = {item["id"] for item in local_data}
    new_entries = [item for item in online_data if item["id"] not in local_ids]

    if new_entries:
        print(f"Found {len(new_entries)} new entries.")
        local_data.extend(new_entries)
        local_data.sort(key=lambda x: x["id"])
        with open(local_file, "w", encoding="utf-8") as f:
            json.dump(local_data, f, ensure_ascii=False, indent=2)
        print(f"Updated {local_file}")
        return True
    else:
        print(f"{local_file} is already up to date.")
        return False


def combine_json(en_file, jp_file, out_file):
    print(f"\nCombining {en_file} + {jp_file} -> {out_file}...")

    with open(en_file, "r", encoding="utf-8") as f:
        en_data = json.load(f)

    with open(jp_file, "r", encoding="utf-8") as f:
        jp_data = json.load(f)

    existing_ids = {item["id"] for item in en_data}
    added = 0

    for item in jp_data:
        if item["id"] not in existing_ids:
            en_data.append(item)
            existing_ids.add(item["id"])
            added += 1

    en_data.sort(key=lambda x: x["id"])

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(en_data, f, ensure_ascii=False, indent=2)

    print(f"Added {added} new items from JP -> {out_file}")


# Run all updates
changed_any = False
for file_info in FILES:
    changed = update_json(file_info["url"], file_info["local"])
    if changed:
        changed_any = True

# Combine EN + JP into merged output files
print("\n--- Combining files ---")
for pair in COMBINE_PAIRS:
    combine_json(pair["en"], pair["jp"], pair["out"])

with open("update_flag.txt", "w") as f:
    f.write("1" if changed_any else "0")

print("\nDone.")