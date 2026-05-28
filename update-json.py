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
    }
]


def update_json(url, local_file):
    print(f"\nChecking {local_file}...")

    # Download latest data
    response = requests.get(url)
    response.raise_for_status()
    online_data = response.json()

    # If local file doesn't exist, create it
    if not Path(local_file).exists():
        with open(local_file, "w", encoding="utf-8") as f:
            json.dump(online_data, f, ensure_ascii=False, indent=2)

        print(f"Created {local_file}")
        return

    # Load local file
    with open(local_file, "r", encoding="utf-8") as f:
        local_data = json.load(f)

    # Existing IDs
    local_ids = {item["id"] for item in local_data}

    # Find new entries
    new_entries = [
        item for item in online_data
        if item["id"] not in local_ids
    ]

    if new_entries:
        print(f"Found {len(new_entries)} new entries.")

        local_data.extend(new_entries)

        # Sort by ID
        local_data.sort(key=lambda x: x["id"])

        # Save updated file
        with open(local_file, "w", encoding="utf-8") as f:
            json.dump(local_data, f, ensure_ascii=False, indent=2)

        print(f"Updated {local_file}")
    else:
        print(f"{local_file} is already up to date.")


# Run all updates
for file_info in FILES:
    update_json(file_info["url"], file_info["local"])

print("\nDone.")