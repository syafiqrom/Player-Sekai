import subprocess
import sys

SCRIPTS = [
    "update-json.py",
    "combine-json.py",
    "download.py",
    "download-jp.py",
    "move-files.py"
]

def run_script(script: str) -> bool:
    print(f"\n=== Running {script} ===")

    result = subprocess.run([sys.executable, script], text=True)

    if result.returncode != 0:
        print(f"ERROR: {script} failed with code {result.returncode}")
        sys.exit(result.returncode)

    print(f"=== Finished {script} ===")
    return True


def main():
    # STEP 1: run update-json first
    print("\n=== STEP 1: update-json ===")
    result = subprocess.run([sys.executable, "update-json.py"], text=True)

    if result.returncode != 0:
        print("update-json failed")
        sys.exit(1)

    # OPTIONAL: detect if update-json printed "already up to date"
    # simplest reliable method: check files instead

    # crude but effective: check git-style diff marker file
    # (recommended: write a flag file instead, see below)

    with open("update_flag.txt", "r") as f:
        changed = f.read().strip() == "1"

    if changed == False:
        print("No updates detected. Skipping remaining scripts.")
        return

    # STEP 2: run rest
    for script in SCRIPTS[1:]:
        run_script(script)

    print("\nAll scripts completed successfully.")


if __name__ == "__main__":
    main()