"""
Resumes Spotify scraping from where it left off.
- Skips any entry that already has a non-null spotifyLink
- Saves musicOriginals2.json after EVERY fetch (incremental — safe to Ctrl+C)
- Re-run anytime to continue from where it stopped

Requirements:
    pip install selenium webdriver-manager

Usage:
    python add_spotify_links_resume.py
"""

import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ── CONFIG ────────────────────────────────────────────────────────────────────
FILE          = "musicOriginals2.json"  # reads AND writes the same file
DELAY_SECONDS = 2.0
HEADLESS      = False   # keep False — Spotify is less likely to block visible browser
# ─────────────────────────────────────────────────────────────────────────────


def make_driver(headless: bool) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )


def handle_cookie_banner(driver):
    try:
        btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[data-testid='cookie-policy-dialog-accept-button']")
            )
        )
        btn.click()
        time.sleep(1)
    except Exception:
        pass


def search_spotify(driver, title: str):
    url = f"https://open.spotify.com/search/{title.replace(' ', '%20')}/tracks"
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[data-testid='tracklist-row']")
            )
        )
        rows = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='tracklist-row']")
        if not rows:
            return None
        link_el = rows[0].find_element(By.CSS_SELECTOR, "a[href*='/track/']")
        href = link_el.get_attribute("href")
        return href.split("?")[0] if href else None
    except Exception:
        return None


def save(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    with open(FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Only process entries with no link yet (null) that have a title
    pending = [e for e in data if e.get("title") and e.get("spotifyLink") is None]
    total_pending = len(pending)

    if total_pending == 0:
        print("All done — every entry already has a Spotify link!")
        return

    print(f"{total_pending} entries still need Spotify links. Starting browser...")

    # Index for fast lookup
    id_to_idx = {e["musicId"]: i for i, e in enumerate(data)}

    driver = make_driver(HEADLESS)
    driver.get("https://open.spotify.com")
    time.sleep(3)
    handle_cookie_banner(driver)

    done = 0
    try:
        for entry in pending:
            title    = entry["title"]
            music_id = entry["musicId"]

            link   = search_spotify(driver, title)
            status = link if link else "not found"

            # Write result back into the main list
            data[id_to_idx[music_id]]["spotifyLink"] = link

            # Save immediately — every single entry
            save(data)

            done += 1
            print(f"[{done}/{total_pending}] musicId={music_id} {title!r:40s} → {status}")

            time.sleep(DELAY_SECONDS)

    except KeyboardInterrupt:
        print(f"\nStopped by user. Progress saved ({done}/{total_pending} done this session).")
    finally:
        driver.quit()

    found = sum(1 for e in data if e.get("spotifyLink"))
    print(f"\nFinished. {found}/{len(data)} total entries have a Spotify link.")


if __name__ == "__main__":
    main()