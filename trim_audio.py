#!/usr/bin/env python3
"""
trim_audio.py
Removes the first 8 seconds from every audio file in a folder tree.
Overwrites originals in-place. Requires ffmpeg on PATH.
"""

import sys
import subprocess
import tempfile
import shutil
from pathlib import Path

TRIM_SECONDS = 8
AUDIO_EXTS = {
    ".mp3", ".wav", ".flac", ".aac",
    ".ogg", ".m4a", ".wma", ".opus",
    ".aiff", ".aif",
}


def trim_file(path: Path) -> tuple[bool, str]:
    tmp = path.with_suffix(".tmp" + path.suffix)
    try:
        result = subprocess.run(
            [
                "ffmpeg", "-y",
                "-ss", str(TRIM_SECONDS),
                "-i", str(path),
                "-c", "copy",
                str(tmp),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            tmp.unlink(missing_ok=True)
            return False, f"  ✗ ffmpeg error: {result.stderr.splitlines()[-1]}"
        shutil.move(str(tmp), str(path))
        return True, "  ✓ trimmed"
    except FileNotFoundError:
        return False, "  ✗ ffmpeg not found — install it and add to PATH"
    except Exception as exc:
        tmp.unlink(missing_ok=True)
        return False, f"  ✗ {exc}"


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    if not root.is_dir():
        print(f"Error: '{root}' is not a directory.")
        sys.exit(1)

    files = [p for p in root.rglob("*") if p.suffix.lower() in AUDIO_EXTS]
    if not files:
        print("No audio files found.")
        sys.exit(0)

    print(f"Found {len(files)} audio file(s) under '{root}'\n")
    ok = fail = 0
    for f in files:
        print(f.name)
        success, msg = trim_file(f)
        print(msg)
        if success:
            ok += 1
        else:
            fail += 1

    print(f"\nDone — {ok} trimmed, {fail} failed.")


if __name__ == "__main__":
    main()