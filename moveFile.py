import os
import shutil
import re

src_folder = "songs"
dst_folder = "Vocaloid"

names = {"Miku", "Len", "Rin", "Kaito", "Meiko", "Luka"}

os.makedirs(dst_folder, exist_ok=True)

def has_exact_name(filename):
    words = re.findall(r'\b\w+\b', filename)
    return any(word in names for word in words)

for file in os.listdir(src_folder):
    if not file.lower().endswith(".mp3"):
        continue

    if has_exact_name(file):
        src_path = os.path.join(src_folder, file)
        dst_path = os.path.join(dst_folder, file)

        shutil.move(src_path, dst_path)
        print(f"Moved: {file}")