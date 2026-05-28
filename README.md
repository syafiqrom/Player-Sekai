# 🎵 Player Sekai

A local **Project Sekai** song player. Browse and play songs from the game directly on your browser — no internet required after setup.

> **All game assets belong to their respective owners.**
> Assets are sourced from [sekai.best](https://sekai.best) (a fan-made website) and the [Sekai World Viewer](https://github.com/Sekai-World/sekai-viewer) project.
> This tool simply automates downloading them for local use.

---

## 📦 Dependencies

### Python
Install required Python packages:

```bash
pip install requests mutagen
```

**Full import list used by the scripts:**
```python
import json
import os
import requests
from mutagen.flac import FLAC
from pathlib import Path
import shutil
```

### VS Code Extension
- [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) — to serve the player in your browser

---

## 🚀 Setup

### 1. Clone the Sekai Viewer (for asset references)

```bash
git clone https://github.com/Sekai-World/sekai-viewer.git
```

### 2. Get up-to-date song data

To fetch the latest songs, grab the JSON files directly from [sekai.best](https://sekai.best/music):

1. Go to [sekai.best/music](https://sekai.best/music)
2. Open DevTools: **Right click → Inspect → Network tab**
3. Search for `musics.json` and `musicVocals.json`
4. Download and replace the existing files in the project:

| Version | Files to replace |
|---|---|
| 🇬🇧 English | `musics.json`, `musicVocals.json` |
| 🇯🇵 Japanese | `musics-jp.json`, `musicVocals-jp.json` |

---

## ▶️ Usage

### Step 1 — Download songs

Open a terminal in the project folder and run:

```bash
# English version
python download.py

# Japanese version
python download-jp.py
```

This will download:
- 🎵 **FLAC audio files** → `audio/` folder
- 🖼️ **Jacket images (WebP)** → `jackets/` folder

---

### Step 2 — Organize songs into group folders *(optional)*

```bash
python move-files.py
```

This moves songs into their respective unit/group subfolders.

---

### Step 3 — Open the player

1. Open the project folder in **VS Code**
2. Right-click on `player.html`
3. Select **"Open with Live Server"**

Your browser will open the player at `http://127.0.0.1:5500/player.html` (or similar).

---

## 📁 Project Structure

```
player-sekai/
├── audio/                 # Downloaded FLAC songs
├── jackets/               # Downloaded WebP jacket art
├── download.py            # Download script (EN)
├── download-jp.py         # Download script (JP)
├── gameCharacters.json    # Game characters metadata
├── outsideCharacters.json # Characters metadata that are not in-game
├── musics.json            # Song metadata (EN)
├── musics-jp.json         # Song metadata (JP)
├── musicVocals.json       # Vocal/unit metadata (EN)
├── musicVocals-jp.json    # Vocal/unit metadata (JP)
├── move-files.py          # Song organizer script
└── player.html            # The music player
```

---

## ⚠️ Disclaimer

This project is a **fan-made tool** for personal use only.
All music and image assets are property of **SEGA** / **Colorful Palette**.
Please support the official game: [Project Sekai Colorful Stage!](https://pjsekai.sega.jp/)
