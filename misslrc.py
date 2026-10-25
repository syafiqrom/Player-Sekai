import json
import os

# ── Config ────────────────────────────────────────────────────────────────────
JSON_FILE  = "musics-jp.json"
LYRICS_DIR = "lyrics"
# ─────────────────────────────────────────────────────────────────────────────

def load_songs(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return data
    for key in ("songs", "data", "items", "music"):
        if key in data and isinstance(data[key], list):
            return data[key]
    raise ValueError(f"Cannot find a song list in {path}. Keys: {list(data.keys())}")


def get_lrc_ids(lyrics_dir: str) -> set[str]:
    """Return a set of stems (filenames without .lrc extension) from the lyrics folder."""
    if not os.path.isdir(lyrics_dir):
        print(f"[ERROR] Lyrics folder not found: {lyrics_dir!r}")
        return set()
    return {
        os.path.splitext(f)[0]
        for f in os.listdir(lyrics_dir)
        if f.lower().endswith(".lrc")
    }


def main():
    print(f"Reading  : {JSON_FILE}")
    print(f"Lyrics   : {LYRICS_DIR}/\n")

    songs = load_songs(JSON_FILE)
    print(f"Total songs in JSON : {len(songs)}")

    lrc_ids = get_lrc_ids(LYRICS_DIR)
    print(f"Total .lrc files    : {len(lrc_ids)}\n")

    missing = [
        song for song in songs
        if str(song.get("id", "")).strip() not in lrc_ids
    ]

    if not missing:
        print("✓ All IDs in JSON have a matching .lrc file.")
        return

    print(f"Missing lyrics ({len(missing)} songs):")
    print(f"{'#':<6} {'ID':<20} TITLE")
    print("─" * 60)
    for i, song in enumerate(missing, 1):
        song_id = song.get("id", "N/A")
        title   = song.get("title", "N/A")
        print(f"{i:<6} {str(song_id):<20} {title}")

    # Also write to a text file for easy reference
    out_file = "missing_lyrics.txt"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(f"Missing lyrics — {len(missing)} songs\n")
        f.write("=" * 60 + "\n")
        for song in missing:
            f.write(f"{song.get('id', 'N/A')} | {song.get('title', 'N/A')}\n")
    print(f"\nSaved to: {out_file}")


if __name__ == "__main__":
    main()