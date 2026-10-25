import subprocess
import sys

def run_librelyrics(links_file="links.txt"):
    try:
        with open(links_file, "r") as f:
            links = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: '{links_file}' not found.")
        sys.exit(1)

    if not links:
        print("No links found in the file.")
        sys.exit(0)

    print(f"Found {len(links)} link(s). Starting librelyrics...\n")

    for i, link in enumerate(links, 1):
        print(f"[{i}/{len(links)}] Running: librelyrics {link}")
        result = subprocess.run(["librelyrics", link])
        if result.returncode != 0:
            print(f"  Warning: librelyrics exited with code {result.returncode} for {link}")
        print()

    print("Done!")

if __name__ == "__main__":
    file = sys.argv[1] if len(sys.argv) > 1 else "links.txt"
    run_librelyrics(file)