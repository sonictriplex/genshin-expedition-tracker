# Genshin Impact Expedition Tracker

Ein plattformübergreifender Tracker für Expeditionen in Genshin Impact – verfügbar als **PyQt6-Desktop-App** und als **native Android-App** mit Jetpack Compose.

A cross‑platform tracker for expeditions in Genshin Impact, available as a **PyQt6 desktop application** and as a **native Android app** built with Jetpack Compose.

---

## Features / Funktionen

### Desktop (PyQt6)

- **Live-Ring-Timer:** Kreisförmige Fortschrittsanzeigen für aktive Expeditionen.
- **Charakter-Boni:** Erkennt automatisch Charaktere mit 25 % Zeitreduktion (z. B. Bennett, Fischl, Chongyun, Keqing, Kujou Sara).
- **Desktop-Benachrichtigungen:** Benachrichtigt über `plyer`, sobald eine Expedition abgeschlossen ist.
- **Operations HQ:** Zeigt die nächste anstehende Expedition, den täglichen Server-Reset (04:00) und einen Harz-Zähler.
- **Alle einsammeln:** Sammelt alle abgeschlossenen Expeditionen auf einmal ein.
- **Persistenz:** Expeditionsdaten werden automatisch in `expeditions.json` gespeichert und beim nächsten Start wiederhergestellt.
- **Charakter-Icons:** Hintergrundbilder der Charaktere werden aus dem Ordner `assets/characters/` geladen (optional).
- **Regionale Themes:** Wähle zwischen sieben Teyvat-Regionen (Mondstadt, Liyue, Inazuma, Sumeru, Fontaine, Natlan, Snezhnaya), die das gesamte Farbschema der App anpassen.
- **System Tray:** Minimieren in die Taskleiste und im Hintergrund weiterlaufen.
- **Autostart:** Option, mit dem System zu starten (Windows-Registry oder Linux-`.desktop`-Datei).
- **Teyvat-Journal:** Tägliche Aufträge, wöchentliche Bosse, Katheryne, Parametrischer Transformator, Artefakt-Route und Endgame-Sternzähler (Abgrund & Theater).
- **Crafting-Rechner:** Alchemie- und Werkbank-Rechner mit passiven Charakter-Boni (Sucrose/Albedo, Mona/Xingqiu).
- **Wunsch- & Pity-Zähler:** Verfolge Pity, Garantie-Status, Primogems und Schicksale.
- **Harz-Planer:** Zeigt die Zeit bis zum vollen Harz-Limit und eine Warnzeit.
- **Wöchentlicher Boss-Tracker:** Verwalte Halb-Harz-Rabatte und besiegte Bosse.
- **Team- & Farm-Ziele:** Plane den Talentbuch-Farmplan für bis zu 4 Charaktere.

### Android (Jetpack Compose)

- **Native UI:** Modernes Material-3-Design mit dunklem Theme.
- **Expeditionsverwaltung:** Hinzufügen, Anzeigen und Löschen von Expeditionen mit einem übersichtlichen Kartenlayout.
- **Harz-Zähler:** Zeigt aktuelles Harz (regeneriert 1 alle 8 Minuten) und die Zeit bis zur vollen Aufladung.
- **Täglicher Reset-Timer:** Zeigt die Zeit bis zum nächsten Server-Reset (04:00).
- **Benachrichtigungen:** Verwendet Androids `WorkManager`, um eine Benachrichtigung zu planen, wenn eine Expedition endet.
- **Persistenz:** Expeditions- und Harzdaten werden in `SharedPreferences` gespeichert und beim nächsten Start wiederhergestellt.
- **Charakterbilder:** Lädt dynamisch Charakter-Drawables aus den App-Ressourcen.
- **Regionale Themes:** Wähle zwischen sieben Teyvat-Regionen (Mondstadt, Liyue, Inazuma, Sumeru, Fontaine, Natlan, Snezhnaya), die das gesamte Farbschema der App anpassen.
- **Crafting-Rechner:** Integrierter Rechner für Alchemie- und Handwerksmaterialien.
- **Wunsch- & Pity-Zähler:** Verfolge Pity und Ersparnisse für Wünsche.
- **Wöchentlicher Boss-Tracker:** Verwalte Halb-Harz-Rabatte und besiegte Bosse.

---

## Installation & Erste Schritte / Installation & Getting Started

### Desktop (Python)

#### Voraussetzungen / Prerequisites

- Python 3.8 oder höher / Python 3.8 or higher
- pip (Python-Paketmanager) / pip (Python package manager)

#### Abhängigkeiten installieren / Install Dependencies

```bash
pip install PyQt6 plyer
```

#### Repository klonen / Clone Repository

```bash
git clone https://github.com/sonictriplex/genshin-expedition-tracker.git
cd genshin-expedition-tracker
```

#### Charakter-Icons herunterladen (optional) / Download Character Icons (optional)

Führe das enthaltene Skript aus, um die 93 Charakter-Icons von Fandom herunterzuladen:

```bash
python download_genshin_icons.py
```

#### Programm starten / Start the Program

```bash
python main.py
```

### Android

#### Voraussetzungen / Prerequisites

- Android Studio (aktuelle Version empfohlen) / Android Studio (latest version recommended)
- Android SDK 26+ (minSdk = 26)
- Gradle 9.5 (im Wrapper enthalten) / Gradle 9.5 (included in wrapper)

#### Build & Run

1. Öffne den Ordner `android/` in Android Studio.
2. Lass Gradle synchronisieren und Abhängigkeiten herunterladen.
3. Verbinde ein Gerät oder starte einen Emulator (API 26+).
4. Klicke auf Run (▶) oder führe aus:

```bash
cd android
./gradlew installDebug
```

---

## Verwendung / Usage

### Desktop

1. Klicke auf „+ Start New Expedition“, um eine neue Expedition zu erstellen.
2. Wähle Charakter, Region, Ressource und Dauer.
3. Der Ring-Timer zeigt den verbleibenden Countdown.
4. Sobald eine Expedition abgeschlossen ist, erscheint eine Desktop-Benachrichtigung (falls `plyer` installiert ist).
5. Klicke auf „Claim Reward“ oder „Claim All Ready“ im Operations HQ, um die Belohnung einzusammeln.
6. Daten werden automatisch gespeichert und beim nächsten Start wiederhergestellt.
7. Theme wechseln: Wähle eine Region aus dem Dropdown-Menü oben rechts, um das gesamte Farbschema der App anzupassen.
8. System Tray: Schließe das Fenster, um in die Taskleiste zu minimieren; nutze das Tray-Icon zum Wiederöffnen oder Beenden.
9. Seitenleisten-Navigation: Nutze die linke Seitenleiste, um zwischen Expeditionen, Teyvat-Journal, Crafting-Rechner, Wunsch- & Pity-Zähler, Harz-Planer, Wöchentlichem Boss-Tracker, Team- & Farm-Zielen und Einstellungen zu wechseln.

### Android

1. Tippe auf „+ Start New Expedition“, um den Hinzufügen-Dialog zu öffnen.
2. Wähle Charakter, Region, Ressource und Dauer (4/8/12/16/20 Stunden).
3. Die Karte zeigt einen Live-Countdown und das Charakterbild.
4. Wenn der Timer Null erreicht, zeigt die Karte „READY!“ und eine Benachrichtigung wird gesendet.
5. Tippe auf „Claim Reward“, um die Expedition zu entfernen.
6. Nutze die Operations-HQ-Karte, um die nächste Ankunft, den täglichen Reset und den Harz-Zähler zu sehen.
7. Tippe auf das Zahnrad-Symbol neben „RESIN COUNTER“, um das Harz manuell anzupassen.
8. Theme wechseln: Tippe auf den Regionsnamen oben rechts, um das gesamte Farbschema der App anzupassen.
9. Nutze die untere Navigation, um auf Tracker, Journal, Crafting, Wishes und Bosses zuzugreifen.

---

## Projektstruktur / Project Structure

```
genshin-expedition-tracker/
├── assets/
│   └── characters/                  # Charakter-Icons / Bilder
├── android/                         # Android-Studio-Projekt
│   └── app/src/main/java/com/mediamatrix/genshintracker/
│       ├── Expedition.kt            # Datenmodelle, Konstanten & SharedPrefs-Logik
│       ├── ExpeditionWorker.kt      # WorkManager für Hintergrund-Timer & Benachrichtigungen
│       ├── MainActivity.kt          # UI, Adapter & Hauptlogik
│       ├── NotificationHelper.kt    # Benachrichtigungskanal & Builder
│       ├── Screens.kt               # Zusätzliche Compose-Screens (Crafting, Wishes, Bosses)
│       └── ui/theme/                # Material-Theme-Definitionen
├── config.py                        # Themes, Pfade, Charakterdaten & plattformübergreifender Autostart
├── crafting.py                      # Crafting-Rechner-Widget (Desktop)
├── dialogs.py                       # Overlay-Dialoge (Expedition hinzufügen, Harz, Einstellungen)
├── journal.py                       # Teyvat-Journal-Widget (Desktop)
├── main.py                          # Hauptfenster, System Tray & App-Einstiegspunkt
├── resin_planner.py                 # Harz-Planer-Widget (Desktop)
├── team_goals.py                    # Team- & Farm-Ziele-Widget (Desktop)
├── weekly_bosses.py                 # Wöchentlicher Boss-Tracker-Widget (Desktop)
├── widgets.py                       # Benutzerdefinierte UI-Widgets (ExpeditionCard, OperationsHQCard)
├── wishes.py                        # Wunsch- & Pity-Zähler-Widget (Desktop)
├── download_genshin_icons.py        # Hilfsskript zum Herunterladen der Charakter-Icons
├── expeditions.json                 # Automatisch erstellte Speicherdatei (Desktop)
└── README.md                        # Projektdokumentation & Git-Info
```

---

## Übersetzungen / Translations

Die zentrale Übersetzungsdatei `translations.py` enthält alle Sprachtexte für die Desktop-Anwendung. Sie unterstützt aktuell **Deutsch** und **Englisch** und kann einfach um weitere Sprachen erweitert werden.

The central translation file `translations.py` contains all UI strings for the desktop application. It currently supports **German** and **English** and can easily be extended with additional languages.

---

## Lizenz & Haftungsausschluss / License & Disclaimer

Dieses Projekt ist unter der MIT-Lizenz lizenziert.

- **Assets & IP:** Alle Charakter-Icons, Spielgrafiken und zugehöriges Material sind Eigentum von HoYoverse.
- Dieses Projekt ist ein inoffizielles, nicht-kommerzielles Fan-Tool, das unter der Fan-Art-Policy von HoYoverse erstellt wurde. Es wird von HoYoverse weder unterstützt, befürwortet noch gesponsert.
- README.md optimiert mit Aider
