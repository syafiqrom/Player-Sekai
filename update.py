import subprocess
import sys

SCRIPTS = [
    "update-json.py",
    "combine-json.py",
    "download.py",
    "download-jp.py"
    "move-files.py"
]

def run_script(script: str) -> None:
    print(f"\n=== Running {script} ===")

    result = subprocess.run(
        [sys.executable, script],
        text=True
    )

    if result.returncode != 0:
        print(f"ERROR: {script} failed with code {result.returncode}")
        sys.exit(result.returncode)

    print(f"=== Finished {script} ===")


def main():
    for script in SCRIPTS:
        run_script(script)

    print("\nAll scripts completed successfully.")


if __name__ == "__main__":
    main()