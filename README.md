# Genshin Impact Expedition Tracker

Ein PyQt6-basierter Desktop-Tracker für Erkundungen in Genshin Impact.

## Features
- **Live Ring-Timer:** Kreisförmige Fortschrittsanzeigen für aktive Erkundungen.
- **Charakter-Boni:** Erkennt automatisch Figuren mit 25% Zeitersparnis (z. B. Bennett, Chongyun, Fischl, Keqing, Shenhe).
- **Desktop Notifications:** Benachrichtigt dich via `plyer`, wenn eine Expedition abgeschlossen ist.
- **Operations HQ:** Zeigt die nächste anstehende Expedition, den täglichen Server-Reset (04:00) und einen Harz-Zähler an.
- **Claim All Ready:** Sammle alle abgeschlossenen Expeditionen auf einmal ein.
- **Persistenz:** Expeditionsdaten werden automatisch in `expeditions.json` gespeichert und beim nächsten Start wiederhergestellt.
- **Charakter-Icons:** Hintergrundbilder der Charaktere werden aus dem Ordner `assets/characters/` geladen (optional).

## Installation & Start

### Voraussetzungen
- Python 3.8 oder höher
- pip (Python-Paketmanager)

### Abhängigkeiten installieren
```bash
pip install PyQt6 plyer
```

### Repository klonen
```bash
git clone https://github.com/sonictriplex/genshin-expedition-tracker.git
cd genshin-expedition-tracker
```

### Charakter-Icons herunterladen (optional)
Führe das beiliegende Skript aus, um die 93 Charakter-Icons von Fandom herunterzuladen:
```bash
python download_genshin_icons.py
```

### Programm starten
```bash
python main.py
```

## Nutzung
1. Klicke auf **„+ Start New Expedition“**, um eine neue Expedition zu erstellen.
2. Wähle einen Charakter, eine Region, eine Ressource und eine Dauer aus.
3. Der Ring-Timer zeigt den verbleibenden Countdown an.
4. Sobald eine Expedition abgeschlossen ist, erscheint eine Desktop-Benachrichtigung (falls `plyer` installiert ist).
5. Klicke auf **„Claim Reward“** oder auf **„Claim All Ready“** im Operations HQ, um die Belohnung einzusammeln.
6. Die Daten werden automatisch gespeichert und beim nächsten Start wiederhergestellt.

## Projektstruktur
```
genshin-expedition-tracker/
├── assets/
│   └── characters/          # Charakter-Icons (optional)
├── main.py                  # Hauptprogramm
├── download_genshin_icons.py # Skript zum Herunterladen der Icons
├── expeditions.json         # Automatisch erstellte Speicherdatei
└── README.md                # Diese Datei
```

## Lizenz
Dieses Projekt ist unter der MIT-Lizenz lizenziert.
