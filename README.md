# Genshin Impact Expedition Tracker

A PyQt6-based desktop tracker for expeditions in Genshin Impact.

## Features
- **Live Ring Timer:** Circular progress indicators for active expeditions.
- **Character Bonuses:** Automatically detects characters with 25% time reduction (e.g., Bennett, Chongyun, Fischl, Keqing, Shenhe).
- **Desktop Notifications:** Notifies you via `plyer` when an expedition is completed.
- **Operations HQ:** Shows the next upcoming expedition, daily server reset (04:00), and a resin counter.
- **Claim All Ready:** Collect all completed expeditions at once.
- **Persistence:** Expedition data is automatically saved to `expeditions.json` and restored on next launch.
- **Character Icons:** Background images of characters are loaded from the `assets/characters/` folder (optional).

## Installation & Startup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Install Dependencies
```bash
pip install PyQt6 plyer
```

### Clone Repository
```bash
git clone https://github.com/sonictriplex/genshin-expedition-tracker.git
cd genshin-expedition-tracker
```

### Download Character Icons (optional)
Run the included script to download the 93 character icons from Fandom:
```bash
python download_genshin_icons.py
```

### Start the Program
```bash
python main.py
```

## Usage
1. Click **„+ Start New Expedition“** to create a new expedition.
2. Select a character, region, resource, and duration.
3. The ring timer shows the remaining countdown.
4. Once an expedition is completed, a desktop notification appears (if `plyer` is installed).
5. Click **„Claim Reward“** or **„Claim All Ready“** in the Operations HQ to collect the reward.
6. Data is automatically saved and restored on next launch.

## Project Structure
```
genshin-expedition-tracker/
├── assets/
│   └── characters/          # Character icons (optional)
├── main.py                  # Main program
├── download_genshin_icons.py # Script to download icons
├── expeditions.json         # Auto‑created save file
└── README.md                # This file
```

## License & Disclaimer

This project is licensed under the MIT License.

* **Assets & IP:** All character icons, game art, and related materials are the property of **HoYoverse**. 
* This project is an unofficial, non-commercial fan-made tool created under HoYoverse's Fan-Art Policy. It is not affiliated with, endorsed, or sponsored by HoYoverse.

README.md optimized with aider
