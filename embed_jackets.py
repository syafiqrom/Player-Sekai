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
from pathlib import Path

from PIL import Image
from mutagen.flac import FLAC, Picture
from mutagen.id3 import PictureType


# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------
# FLAC files are named {assetbundleName}.flac (e.g. "light_sound_0001_01.flac")
# Jacket files are named {assetbundleName}.webp (e.g. "light_sound_0001.webp")
# We match by stripping the last "_NN" vocal-variant suffix from the FLAC stem
# to get the shared assetbundleName prefix used by the jacket.
FLAC_VOCAL_SUFFIX = re.compile(r"_\d{2}$")


def jacket_key_from_flac(stem: str) -> str:
    """Strip the trailing vocal-variant suffix (e.g. _01) to get the jacket stem."""
    return FLAC_VOCAL_SUFFIX.sub("", stem)


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

def build_jacket_map(jackets_dir: Path) -> dict[str, Path]:
    """Map assetbundleName stem -> jacket Path for every .webp in jackets_dir."""
    mapping: dict[str, Path] = {}
    for p in jackets_dir.glob("*.webp"):
        mapping[p.stem] = p
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
        raise FileNotFoundError(f"audio directory not found: {audio_dir}")
    if not jackets_dir.is_dir():
        raise FileNotFoundError(f"jackets directory not found: {jackets_dir}")

    jacket_map = build_jacket_map(jackets_dir)
    if not jacket_map:
        raise FileNotFoundError("No jacket images found (expected {assetbundleName}.webp)")

    print(f"Found {len(jacket_map)} jacket image(s) in '{jackets_dir}'.\n")

    matched = unmatched = skipped = 0

    for flac_path in sorted(audio_dir.rglob("*.flac")):
        key = jacket_key_from_flac(flac_path.stem)
        jacket = jacket_map.get(key)
        if jacket is None:
            # Fallback: try the full stem (no suffix to strip)
            jacket = jacket_map.get(flac_path.stem)

        if jacket is None:
            print(f"  [MISS]  No jacket for '{key}'  ({flac_path.name})")
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

    try:
        process(
            audio_dir   = Path(args.audio),
            jackets_dir = Path(args.jackets),
            dry_run     = args.dry_run,
        )
    except FileNotFoundError as e:
        import sys
        sys.exit(f"ERROR: {e}")


if __name__ == "__main__":
    main()