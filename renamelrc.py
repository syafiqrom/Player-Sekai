import json
import os

# ── Config ────────────────────────────────────────────────────────────────────
JSON_FILE   = "musics-jp.json"
LYRICS_DIR  = "lyrics"
DRY_RUN     = False   # Set True to preview changes without renaming
# ─────────────────────────────────────────────────────────────────────────────

def load_songs(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    # Support both a bare list and {"songs": [...]} / {"data": [...]} wrappers
    if isinstance(data, list):
        return data
    for key in ("songs", "data", "items", "music"):
        if key in data and isinstance(data[key], list):
            return data[key]
    raise ValueError(f"Cannot find a song list in {path}. Keys: {list(data.keys())}")


def build_title_map(songs: list[dict]) -> dict[str, str]:
    """Return {title_lowercase: id} for every song that has both keys."""
    mapping = {}
    for song in songs:
        title = song.get("title")
        song_id = song.get("id")
        if title and song_id:
            mapping[title.strip().lower()] = str(song_id)
    return mapping


def rename_lyrics(lyrics_dir: str, title_map: dict[str, str], dry_run: bool) -> None:
    if not os.path.isdir(lyrics_dir):
        print(f"[ERROR] Lyrics folder not found: {lyrics_dir!r}")
        return

    lrc_files = [f for f in os.listdir(lyrics_dir) if f.lower().endswith(".lrc")]
    if not lrc_files:
        print(f"[WARN]  No .lrc files found in {lyrics_dir!r}")
        return

    matched   = 0
    unmatched = []

    for filename in sorted(lrc_files):
        stem = os.path.splitext(filename)[0].strip().lower()
        song_id = title_map.get(stem)

        if song_id:
            old_path = os.path.join(lyrics_dir, filename)
            new_name = f"{song_id}.lrc"
            new_path = os.path.join(lyrics_dir, new_name)

            if old_path == new_path:
                print(f"[SKIP]  Already named correctly: {filename}")
                continue

            if dry_run:
                print(f"[DRY]   {filename}  →  {new_name}")
            else:
                os.rename(old_path, new_path)
                print(f"[OK]    {filename}  →  {new_name}")
            matched += 1
        else:
            unmatched.append(filename)

    print(f"\n── Summary ───────────────────────────────")
    print(f"  Matched   : {matched}")
    print(f"  Unmatched : {len(unmatched)}")
    if unmatched:
        print("\n  Files with no matching title in JSON:")
        for f in unmatched:
            print(f"    • {f}")


def main():
    print(f"Reading  : {JSON_FILE}")
    print(f"Lyrics   : {LYRICS_DIR}/")
    print(f"Dry run  : {DRY_RUN}\n")

    songs     = load_songs(JSON_FILE)
    title_map = build_title_map(songs)
    print(f"Loaded {len(songs)} songs, {len(title_map)} with valid title+id.\n")

    rename_lyrics(LYRICS_DIR, title_map, DRY_RUN)


if __name__ == "__main__":
    main()