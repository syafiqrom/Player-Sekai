import os
from pykakasi import kakasi

folder = "songs"

kks = kakasi()
kks.setMode("J", "a")  # Japanese → ascii
kks.setMode("H", "a")  # Hiragana → ascii
kks.setMode("K", "a")  # Katakana → ascii
kks.setMode("r", "Hepburn")  # romaji system
kks.setMode("s", True)  # add spaces
conv = kks.getConverter()

for filename in os.listdir(folder):
    if not filename.lower().endswith(".mp3"):
        continue

    name, ext = os.path.splitext(filename)

    # convert to romaji
    romaji = conv.do(name)

    # cleanup
    romaji = romaji.replace(" ", "_")
    romaji = romaji.strip()

    old_path = os.path.join(folder, filename)
    new_path = os.path.join(folder, romaji + ext)

    if old_path != new_path:
        os.rename(old_path, new_path)
        print(f"{filename} -> {romaji + ext}")