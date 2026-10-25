import json

with open("musicOriginals.json", "r", encoding="utf-8") as f:
    data = json.load(f)

links = [entry["spotifyLink"] for entry in data if entry.get("spotifyLink")]

with open("splinks.txt", "w") as f:
    f.write("\n".join(links))

print(f"Done! Extracted {len(links)} Spotify links to splinks.txt")