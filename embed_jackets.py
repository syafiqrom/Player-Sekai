"""
embed_jackets.py
----------------
Matches jacket images to FLAC audio files by music ID and embeds them
as cover art (converted to JPEG for maximum player compatibility).

File name patterns:
  FLAC  : 0000_00  or  xx_0000_00   (the 4-digit block is the music ID)
  WebP  : jacket_s_000              (the 3-digit suffix is the music ID)

Usage:
  python embed_jackets.py                      # defaults: audio/ and jackets/
  python embed_jackets.py --audio audio --jackets jackets
  python embed_jackets.py --audio audio --jackets jackets --dry-run
"""

import argparse
import io
import re
import sys
from pathlib import Path

from PIL import Image
from mutagen.flac import FLAC, Picture
from mutagen.id3 import PictureType


# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------
FLAC_PATTERN = re.compile(r"(?:[A-Za-z]+_)?(\d{4})_\d{2}$", re.IGNORECASE)
WEBP_PATTERN = re.compile(r"jacket_s_(\d+)$", re.IGNORECASE)


def music_id_from_flac(stem: str) -> str | None:
    m = FLAC_PATTERN.match(stem)
    return m.group(1) if m else None


def music_id_from_webp(stem: str) -> str | None:
    m = WEBP_PATTERN.match(stem)
    return m.group(1) if m else None


def normalise_id(raw: str) -> int:
    return int(raw)


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

def build_jacket_map(jackets_dir: Path) -> dict[int, Path]:
    mapping: dict[int, Path] = {}
    for p in jackets_dir.glob("*.webp"):
        raw = music_id_from_webp(p.stem)
        if raw is not None:
            mapping[normalise_id(raw)] = p
        else:
            print(f"  [SKIP]  Unrecognised jacket filename: {p.name}")
    return mapping


def webp_to_jpeg_bytes(image_path: Path, quality: int = 100) -> bytes:
    """Convert a WebP (or any image) to JPEG bytes in memory."""
    img = Image.open(image_path).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=quality)
    return buf.getvalue()


def embed_cover(flac_path: Path, image_path: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"  [DRY]   Would embed {image_path.name} -> {flac_path}")
        return

    # Convert WebP -> JPEG so every player recognises it
    jpeg_bytes = webp_to_jpeg_bytes(image_path)

    audio = FLAC(flac_path)
    audio.clear_pictures()

    pic = Picture()
    pic.type = PictureType.COVER_FRONT   # 3 = front cover
    pic.mime = "image/jpeg"
    pic.desc = "Cover"
    pic.data = jpeg_bytes

    audio.add_picture(pic)
    audio.save()
    print(f"  [OK]    {flac_path.name}  <-  {image_path.name}")


def process(audio_dir: Path, jackets_dir: Path, dry_run: bool) -> None:
    if not audio_dir.is_dir():
        sys.exit(f"ERROR: audio directory not found: {audio_dir}")
    if not jackets_dir.is_dir():
        sys.exit(f"ERROR: jackets directory not found: {jackets_dir}")

    jacket_map = build_jacket_map(jackets_dir)
    if not jacket_map:
        sys.exit("ERROR: No jacket images found (expected jacket_s_NNN.webp)")

    print(f"Found {len(jacket_map)} jacket image(s) in '{jackets_dir}'.\n")

    matched = unmatched = skipped = 0

    for flac_path in sorted(audio_dir.rglob("*.flac")):
        raw_id = music_id_from_flac(flac_path.stem)
        if raw_id is None:
            print(f"  [SKIP]  Unrecognised FLAC filename: {flac_path.name}")
            skipped += 1
            continue

        mid = normalise_id(raw_id)
        jacket = jacket_map.get(mid)

        if jacket is None:
            print(f"  [MISS]  No jacket for music ID {mid:04d}  ({flac_path.name})")
            with open("log-jacket.txt", "a", encoding="utf-8") as log_file:
                log_file.write(f"{flac_path.name}\n")
            unmatched += 1
            continue

        embed_cover(flac_path, jacket, dry_run)
        matched += 1

    print(f"\nDone.  matched={matched}  unmatched={unmatched}  skipped={skipped}")
    if dry_run:
        print("(dry-run — no files were modified)")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Embed jacket WebP images into FLAC files.")
    parser.add_argument("--audio",   default="audio/theme_park",   help="Root folder containing sub-folders of FLAC files (default: audio)")
    parser.add_argument("--jackets", default="jackets", help="Folder containing jacket_s_NNN.webp files (default: jackets)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without modifying any files")
    args = parser.parse_args()

    process(
        audio_dir   = Path(args.audio),
        jackets_dir = Path(args.jackets),
        dry_run     = args.dry_run,
    )


if __name__ == "__main__":
    main()