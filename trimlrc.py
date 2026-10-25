import os
import re
from pathlib import Path


def rename_lrc_files(folder: str = None) -> None:
    if folder is None:
        folder = Path("lyrics")
    else:
        folder = Path(folder)

    if not folder.exists():
        print(f"Folder not found: {folder}")
        return

    lrc_files = list(folder.glob("*.lrc"))

    if not lrc_files:
        print("No .lrc files found.")
        return

    renamed = 0
    skipped = 0

    for filepath in sorted(lrc_files):
        stem = filepath.stem  # filename without extension

        # Match " (feat." (case-insensitive) and trim everything from it onward
        match = re.search(r'\s*\(feat\.', stem, re.IGNORECASE)
        if not match:
            skipped += 1
            continue

        new_stem = stem[:match.start()].rstrip()
        new_name = new_stem + ".lrc"
        new_path = filepath.parent / new_name

        if new_path.exists():
            print(f"  SKIP (target exists): {filepath.name!r} -> {new_name!r}")
            skipped += 1
            continue

        print(f"  Renaming: {filepath.name!r}")
        print(f"       -> : {new_name!r}")
        filepath.rename(new_path)
        renamed += 1

    print(f"\nDone. {renamed} file(s) renamed, {skipped} skipped.")


if __name__ == "__main__":
    import sys
    folder_arg = sys.argv[1] if len(sys.argv) > 1 else None
    rename_lrc_files(folder_arg)