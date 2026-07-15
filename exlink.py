import json

# Read JSON file
with open("musicOriginals.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract all video links
links = [item["videoLink"] for item in data if "videoLink" in item]

# Save to TXT file (one link per line, no quotes)
with open("video_links.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(links))

print(f"Saved {len(links)} links to video_links.txt")