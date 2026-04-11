import os
import re
from collections import defaultdict

FOLDER = "songs"

# group definitions
groups = {
    "L/N": {"Ichika", "Saki", "Honami", "Shiho"},
    "MMJ": {"Minori", "Haruka", "Airi", "Shizuku"},
    "VBS": {"Kohane", "An", "Akito", "Toya"},
    "WXS": {"Tsukasa", "Emu", "Nene", "Rui"},
    "N25": {"Kanade", "Mafuyu", "Ena", "Mizuki"},
    "Vocaloid": {"Miku", "Rin", "Len", "Luka", "Meiko", "Kaito"},
}

# reverse map: name -> group
name_to_group = {}
for g, names in groups.items():
    for n in names:
        name_to_group[n] = g

result = defaultdict(list)
duplicates = []

def extract_names(filename):
    # "Title - A, B & C.mp3"
    base = os.path.splitext(filename)[0]
    if " - " not in base:
        return []
    part = base.split(" - ", 1)[1]

    # split by ", " and " & "
    names = re.split(r", | & ", part)
    return [n.strip() for n in names if n.strip()]

for file in os.listdir(FOLDER):
    if not file.endswith(".mp3"):
        continue

    names = extract_names(file)
    file_groups = set()

    for n in names:
        g = name_to_group.get(n)
        if g:
            file_groups.add(g)

    # remove Vocaloid for rule 2 check
    non_vocaloid = {g for g in file_groups if g != "Vocaloid"}

    if len(file_groups) == 1:
        # rule 1
        g = next(iter(file_groups))
        result[g].append(file)

    elif len(non_vocaloid) == 1:
        # rule 2
        g = next(iter(non_vocaloid))
        result[g].append(file)

    else:
        # rule 3
        duplicates.append(file)

# write output
with open("grouping.txt", "w", encoding="utf-8") as f:
    for g in groups.keys():
        f.write(f"[{g}]\n")
        for song in sorted(result[g]):
            f.write(f"{song}\n")
        f.write("\n")

    f.write("[DUPLICATE]\n")
    for song in sorted(duplicates):
        f.write(f"{song}\n")

print("Done")