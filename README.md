# Genshin Impact Expedition Tracker

Ein plattformübergreifender Tracker für Expeditionen in Genshin Impact, verfügbar als **PyQt6 Desktop-Anwendung** und als **native Android-App** mit Jetpack Compose.

## Funktionen

### Desktop (PyQt6)
- **Live-Ring-Timer:** Kreisförmige Fortschrittsanzeigen für aktive Expeditionen.
- **Charakter-Boni:** Erkennt automatisch Charaktere mit 25 % Zeitersparnis (z. B. Bennett, Fischl, Chongyun, Keqing, Kujou Sara).
- **Desktop-Benachrichtigungen:** Benachrichtigt über `plyer`, wenn eine Expedition abgeschlossen ist.
- **Operations HQ:** Zeigt die nächste anstehende Expedition, den täglichen Server-Reset (04:00) und einen Harz-Zähler.
- **Alle einsammeln:** Sammle alle abgeschlossenen Expeditionen auf einmal ein.
- **Persistenz:** Expeditionsdaten werden automatisch in `expeditions.json` gespeichert und beim nächsten Start wiederhergestellt.
- **Charakter-Icons:** Hintergrundbilder der Charaktere werden aus dem Ordner `assets/characters/` geladen (optional).
- **Regionale Themes:** Wähle zwischen sieben Teyvat-Regionen (Mondstadt, Liyue, Inazuma, Sumeru, Fontaine, Natlan, Snezhnaya), die das gesamte Farbschema der App anpassen.

### Android (Jetpack Compose)
- **Native UI:** Modernes Material 3 Design mit dunklem Theme.
- **Expeditionsverwaltung:** Hinzufügen, Anzeigen und Löschen von Expeditionen mit einem übersichtlichen Kartenlayout.
- **Harz-Zähler:** Zeigt das aktuelle Harz an (regeneriert 1 alle 8 Minuten) und die Zeit bis zur vollen Aufladung.
- **Täglicher Reset-Timer:** Zeigt die Zeit bis zum nächsten Server-Reset (04:00) an.
- **Benachrichtigungen:** Verwendet Android’s `WorkManager`, um eine Benachrichtigung zu planen, wenn eine Expedition endet.
- **Persistenz:** Expeditions- und Harzdaten werden in `SharedPreferences` gespeichert und beim nächsten Start wiederhergestellt.
- **Charakterbilder:** Lädt dynamisch Charakter-Drawables aus den App-Ressourcen.
- **Regionale Themes:** Wähle zwischen sieben Teyvat-Regionen (Mondstadt, Liyue, Inazuma, Sumeru, Fontaine, Natlan, Snezhnaya), die das gesamte Farbschema der App anpassen.

## Installation & Start

### Desktop (Python)

#### Voraussetzungen
- Python 3.8 oder höher
- pip (Python-Paketmanager)

#### Abhängigkeiten installieren
```bash
pip install PyQt6 plyer
```

#### Repository klonen
```bash
git clone https://github.com/sonictriplex/genshin-expedition-tracker.git
cd genshin-expedition-tracker
```

#### Charakter-Icons herunterladen (optional)
Führe das enthaltene Skript aus, um die 93 Charakter-Icons von Fandom herunterzuladen:
```bash
python download_genshin_icons.py
```

#### Programm starten
```bash
python main.py
```

### Android

#### Voraussetzungen
- Android Studio (aktuelle Version empfohlen)
- Android SDK 26+ (minSdk = 26)
- Gradle 9.5 (im Wrapper enthalten)

#### Build & Ausführen
1. Öffne den Ordner `android/` in Android Studio.
2. Lass Gradle synchronisieren und die Abhängigkeiten herunterladen.
3. Verbinde ein Gerät oder starte einen Emulator (API 26+).
4. Klicke auf **Run** (▶) oder führe aus:
   ```bash
   cd android
   ./gradlew installDebug
   ```

## Verwendung

### Desktop
1. Klicke auf **„+ Start New Expedition“**, um eine neue Expedition zu erstellen.
2. Wähle einen Charakter, eine Region, eine Ressource und eine Dauer aus.
3. Der Ring-Timer zeigt den verbleibenden Countdown an.
4. Sobald eine Expedition abgeschlossen ist, erscheint eine Desktop-Benachrichtigung (falls `plyer` installiert ist).
5. Klicke auf **„Claim Reward“** oder **„Claim All Ready“** im Operations HQ, um die Belohnung einzusammeln.
6. Die Daten werden automatisch gespeichert und beim nächsten Start wiederhergestellt.
7. **Theme wechseln:** Wähle oben rechts im Dropdown-Menü eine Region aus, um das gesamte Farbschema der App anzupassen.

#### Screenshot:

![Screenshot Linux App](./assets/GenshinTrackerLinux.png)

### Android
1. Tippe auf **„+ Start New Expedition“**, um den Hinzufügen-Dialog zu öffnen.
2. Wähle einen Charakter, eine Region, eine Ressource und eine Dauer (4/8/12/16/20 Stunden).
3. Die Karte zeigt einen Live-Countdown und das Bild des Charakters.
4. Wenn der Timer Null erreicht, zeigt die Karte **„READY!“** an und eine Benachrichtigung wird gesendet.
5. Tippe auf **„Claim Reward“**, um die Expedition zu entfernen.
6. Verwende die **Operations HQ**-Karte, um die nächste Ankunft, den täglichen Reset und den Harz-Zähler zu sehen.
7. Tippe auf das Zahnrad-Symbol neben **RESIN COUNTER**, um das Harz manuell anzupassen.
8. **Theme wechseln:** Tippe oben rechts auf den Region-Namen, um das gesamte Farbschema der App anzupassen.

#### Screenshot:

<img src="./assets/GenshinTrackerAndroid.jpg" alt="Screenshot Android App" width="400">

## Projektstruktur

```
genshin-expedition-tracker/
├── assets/
│   └── characters/          # Charakter-Icons (optional, Desktop)
├── main.py                  # Desktop-Hauptprogramm (PyQt6)
├── download_genshin_icons.py # Skript zum Herunterladen der Icons
├── expeditions.json         # Automatisch erstellte Speicherdatei (Desktop)
├── android/                 # Android-Projektwurzel
│   ├── app/
│   │   ├── src/
│   │   │   ├── main/
│   │   │   │   ├── java/com/mediamatrix/genshintracker/
│   │   │   │   │   ├── MainActivity.kt          # Hauptaktivität mit Compose UI
│   │   │   │   │   ├── Expedition.kt            # Datenmodell & Charakterliste
│   │   │   │   │   ├── ExpeditionWorker.kt      # WorkManager-Worker für Benachrichtigungen
│   │   │   │   │   ├── NotificationHelper.kt    # Benachrichtigungskanal & Helfer
│   │   │   │   │   └── ui/theme/                # Material 3 Theme-Dateien
│   │   │   │   ├── res/
│   │   │   │   │   ├── drawable/                # Charakterbilder & Launcher-Icons
│   │   │   │   │   ├── mipmap-*/                # Launcher-Icons
│   │   │   │   │   ├── values/                  # strings.xml, colors.xml, themes.xml
│   │   │   │   │   └── xml/                     # Backup- & Datenextraktionsregeln
│   │   │   │   └── AndroidManifest.xml
│   │   │   ├── androidTest/                     # Instrumentierte Tests
│   │   │   └── test/                            # Unit-Tests
│   │   └── build.gradle.kts
│   ├── build.gradle.kts                         # Top-Level-Build-Datei
│   ├── settings.gradle.kts
│   ├── gradle.properties
│   ├── gradle/
│   │   ├── libs.versions.toml                   # Versionskatalog
│   │   └── wrapper/                             # Gradle Wrapper
│   └── gradlew / gradlew.bat
└── README.md                # Diese Datei
```

## Lizenz & Haftungsausschluss

Dieses Projekt ist unter der MIT-Lizenz lizenziert.

* **Assets & IP:** Alle Charakter-Icons, Spielgrafiken und zugehöriges Material sind Eigentum von **HoYoverse**.
* Dieses Projekt ist ein inoffizielles, nicht-kommerzielles Fan-Tool, das unter der Fan-Art-Richtlinie von HoYoverse erstellt wurde. Es wird nicht von HoYoverse unterstützt, befürwortet oder gesponsert.

* README.md optimiert mit Aider
