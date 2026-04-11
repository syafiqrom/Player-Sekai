import os

folder = "songs"

for filename in os.listdir(folder):
    if not filename.lower().endswith(".mp3"):
        continue

    name, ext = os.path.splitext(filename)

    words = name.split(" ")

    old = "Juuon Teto"
    new = "Teto"
    new_words = [new if w == old else w for w in words]

    new_name = " ".join(new_words) + ext

    old_path = os.path.join(folder, filename)
    new_path = os.path.join(folder, new_name)

    if old_path != new_path:
        os.rename(old_path, new_path)
        print(f"{filename} -> {new_name}")