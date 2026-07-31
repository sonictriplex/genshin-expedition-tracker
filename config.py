import os
import sys

# Platform Check
IS_WINDOWS = sys.platform.startswith("win")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "characters")
SAVE_FILE = os.path.join(BASE_DIR, "expeditions.json")

# Linux XDG Autostart Pfad
AUTOSTART_DIR = os.path.expanduser("~/.config/autostart")
AUTOSTART_FILE = os.path.join(AUTOSTART_DIR, "genshin-expedition-tracker.desktop")
AUTOSTART_REG_KEY = "GenshinExpeditionTracker"

# Regionales Theme-System für Teyvat
REGION_THEMES = {
    "Mondstadt (Anemo)": {
        "cyan": "#38e3e3",
        "amber": "#ffaa00",
        "bg_dark": "#1a1c24",
        "card_bg": "#252833",
    },
    "Liyue (Geo)": {
        "cyan": "#e6a000",
        "amber": "#ffd266",
        "bg_dark": "#221d14",
        "card_bg": "#30291d",
    },
    "Inazuma (Electro)": {
        "cyan": "#a855f7",
        "amber": "#f0abfc",
        "bg_dark": "#1a1325",
        "card_bg": "#251b36",
    },
    "Sumeru (Dendro)": {
        "cyan": "#22c55e",
        "amber": "#facc15",
        "bg_dark": "#122017",
        "card_bg": "#1a2e21",
    },
    "Fontaine (Hydro)": {
        "cyan": "#38bdf8",
        "amber": "#f472b6",
        "bg_dark": "#111c28",
        "card_bg": "#182838",
    },
    "Natlan (Pyro)": {
        "cyan": "#ef4444",
        "amber": "#fbbf24",
        "bg_dark": "#241313",
        "card_bg": "#331c1c",
    },
    "Snezhnaya (Cryo)": {
        "cyan": "#99f6e4",
        "amber": "#a5f3fc",
        "bg_dark": "#121d24",
        "card_bg": "#1a2933",
    },
}

CURRENT_THEME = REGION_THEMES["Mondstadt (Anemo)"]

def set_active_theme(theme_name: str):
    global CURRENT_THEME
    CURRENT_THEME = REGION_THEMES.get(theme_name, REGION_THEMES["Mondstadt (Anemo)"])

def get_theme():
    return CURRENT_THEME

# Charaktere als einfache Liste
CHARACTERS = [
    "Albedo", "Alhaitham", "Aloy", "Amber", "Arataki Itto", "Arlecchino",
    "Barbara", "Baizhu", "Beidou", "Bennett", "Candace", "Charlotte", "Chasca",
    "Chevreuse", "Chiori", "Chongyun", "Citlali", "Clorinde", "Collei",
    "Cyno", "Dehya", "Diluc", "Diona", "Dori", "Emilie", "Eula", "Faruzan",
    "Fischl", "Freminet", "Furina", "Gaming", "Ganyu", "Gorou", "Hu Tao",
    "Iansan", "Jean", "Kachina", "Kaedehara Kazuha", "Kaeya", "Kamisato Ayaka",
    "Kamisato Ayato", "Kaveh", "Keqing", "Kinich", "Kirara", "Klee",
    "Kujou Sara", "Kuki Shinobu", "Lan Yan", "Layla", "Lisa",
    "Lynette", "Lyney", "Mavuika", "Mika", "Mona", "Mualani", "Nahida",
    "Navia", "Neuvillette", "Nilou", "Ningguang", "Noelle", "Ororon",
    "Qiqi", "Raiden Shogun", "Razor", "Rosaria", "Sangonomiya Kokomi",
    "Sayu", "Sethos", "Shenhe", "Shikanoin Heizou", "Sigewinne", "Sucrose",
    "Tartaglia", "Thoma", "Tighnari", "Traveller", "Venti", "Wanderer", "Wriothesley",
    "Xiangling", "Xianyun", "Xiao", "Xilonen", "Xingqiu", "Xinyan",
    "Yae Miko", "Yanfei", "Yaoyao", "Yelan", "Yoimiya", "Yun Jin", "Zhongli",
]

# Charaktere mit 25% Zeitersparnis und ihre Heimatregion
TIME_REDUCTION_BONUS = {
    "Bennett": "Mondstadt",
    "Fischl": "Mondstadt",
    "Chongyun": "Liyue",
    "Keqing": "Liyue",
    "Kujou Sara": "Inazuma",
}

REGIONS = ["Mondstadt", "Liyue", "Inazuma", "Sumeru", "Fontaine", "Natlan"]
RESOURCES = [
    "Mora",
    "Ores (Iron & Crystal)",
    "Meat & Fowl",
    "Ingredients & Plants",
    "Fish",
]

# --- Cross-Platform Autostart Integration ---
def is_autostart_enabled() -> bool:
    if IS_WINDOWS:
        from PyQt6.QtCore import QSettings
        settings = QSettings(
            "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            QSettings.Format.NativeFormat,
        )
        return settings.contains(AUTOSTART_REG_KEY)
    else:
        return os.path.exists(AUTOSTART_FILE)

def set_autostart(enable: bool):
    script_path = os.path.abspath(os.path.join(BASE_DIR, "main.py"))
    python_executable = sys.executable

    if IS_WINDOWS:
        from PyQt6.QtCore import QSettings
        settings = QSettings(
            "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            QSettings.Format.NativeFormat,
        )
        if enable:
            app_path = f'"{python_executable}" "{script_path}"'
            settings.setValue(AUTOSTART_REG_KEY, app_path)
        else:
            if settings.contains(AUTOSTART_REG_KEY):
                settings.remove(AUTOSTART_REG_KEY)
    else:
        if enable:
            if not os.path.exists(AUTOSTART_DIR):
                os.makedirs(AUTOSTART_DIR, exist_ok=True)
            content = f"""[Desktop Entry]
Type=Application
Name=Genshin Expedition Tracker
Exec="{python_executable}" "{script_path}"
Terminal=false
Categories=Utility;Game;
X-GNOME-Autostart-enabled=true
"""
            with open(AUTOSTART_FILE, "w", encoding="utf-8") as f:
                f.write(content)
        else:
            if os.path.exists(AUTOSTART_FILE):
                os.remove(AUTOSTART_FILE)