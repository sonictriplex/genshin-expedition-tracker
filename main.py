import json
import os
import sys
import time

try:
    from plyer import notification
except ImportError:
    notification = None

from PyQt6.QtCore import QRectF, QSize, Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QPainter, QPen, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

# --- Pfade & Farben ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "characters")
SAVE_FILE = os.path.join(BASE_DIR, "expeditions.json")

CORE_COLOR_CYAN = "#38e3e3"
CORE_COLOR_AMBER = "#ffaa00"
BG_COLOR_DARK = "#1a1c24"
CARD_BG_COLOR = "#252833"

# Vollständige Charakterliste mit Erkundungs-Zeitbonus (True = 25% schneller)
CHARACTERS = {
    "Albedo": False,
    "Alhaitham": False,
    "Aloy": False,
    "Amber": False,
    "Arataki Itto": False,
    "Arlecchino": False,
    "Barbara": False,
    "Beidou": False,
    "Bennett": True,
    "Candace": False,
    "Charlotte": False,
    "Chasca": False,
    "Chevreuse": False,
    "Chiori": False,
    "Chongyun": True,
    "Citlali": False,
    "Clorinde": False,
    "Collei": False,
    "Cyno": False,
    "Dehya": False,
    "Diluc": False,
    "Diona": False,
    "Dori": False,
    "Emilie": False,
    "Eula": False,
    "Faruzan": False,
    "Fischl": True,
    "Freminet": False,
    "Furina": False,
    "Gaming": False,
    "Ganyu": False,
    "Gorou": False,
    "Hu Tao": False,
    "Iansan": False,
    "Jean": False,
    "Kachina": False,
    "Kaedehara Kazuha": False,
    "Kaeya": False,
    "Kamisato Ayaka": False,
    "Kamisato Ayato": False,
    "Kaveh": False,
    "Keqing": True,
    "Kinich": False,
    "Kirara": False,
    "Klee": False,
    "Kujou Sara": False,
    "Kuki Shinobu": False,
    "Lan Yan": False,
    "Lanyan": False,
    "Layla": False,
    "Lisa": False,
    "Lynette": False,
    "Lyney": False,
    "Mavuika": False,
    "Mika": False,
    "Mona": False,
    "Mualani": False,
    "Nahida": False,
    "Navia": False,
    "Neuvillette": False,
    "Nilou": False,
    "Ningguang": False,
    "Noelle": False,
    "Ororon": False,
    "Qiqi": False,
    "Raiden Shogun": False,
    "Razor": False,
    "Rosaria": False,
    "Sangonomiya Kokomi": False,
    "Sayu": False,
    "Sethos": False,
    "Shenhe": True,
    "Shikanoin Heizou": False,
    "Sigewinne": False,
    "Sucrose": False,
    "Thoma": False,
    "Tighnari": False,
    "Traveller": False,
    "Venti": False,
    "Wanderer": False,
    "Wriothesley": False,
    "Xiangling": False,
    "Xianyun": False,
    "Xiao": False,
    "Xilonen": False,
    "Xingqiu": False,
    "Xinyan": False,
    "Yae Miko": False,
    "Yanfei": False,
    "Yao Yao": False,
    "Yelan": False,
    "Yoimiya": False,
    "Yun Jin": False,
    "Zhongli": False,
}

REGIONS = ["Mondstadt", "Liyue", "Inazuma", "Sumeru", "Fontaine", "Natlan"]


# =========================================================
# Custom Widget: Der kreisförmige Ring-Timer (QPainter)
# =========================================================
class CircularProgressTimer(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(140, 140)
        self.total_seconds = 1
        self.remaining_seconds = 1
        self.is_complete = False

    def set_time(self, remaining, total):
        self.remaining_seconds = remaining
        self.total_seconds = total
        self.is_complete = remaining <= 0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()
        size = min(width, height) - 16
        rect = QRectF((width - size) / 2, (height - size) / 2, size, size)

        pen_width = 8

        # 1. Hintergrund-Kreis
        bg_pen = QPen(QColor("#1a1c24"), pen_width)
        bg_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawEllipse(rect)

        # 2. Fortschritts-Bogen
        color = (
            QColor(CORE_COLOR_AMBER) if self.is_complete else QColor(CORE_COLOR_CYAN)
        )
        fg_pen = QPen(color, pen_width)
        fg_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(fg_pen)

        if self.total_seconds > 0 and not self.is_complete:
            progress_ratio = self.remaining_seconds / self.total_seconds
            angle = int(-360 * progress_ratio * 16)
            painter.drawArc(rect, 90 * 16, angle)
        elif self.is_complete:
            painter.drawArc(rect, 0, 360 * 16)

        # 3. Zeit-Text in der Mitte
        painter.setPen(color)
        font = QFont("Segoe UI", 13, QFont.Weight.Bold)
        painter.setFont(font)

        if self.is_complete:
            time_str = "FERTIG!"
        else:
            h = max(0, self.remaining_seconds) // 3600
            m = (max(0, self.remaining_seconds) % 3600) // 60
            s = max(0, self.remaining_seconds) % 60
            time_str = f"{h:02d}:{m:02d}:{s:02d}"

        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, time_str)


# =========================================================
# Custom Widget: Die Expeditions-Karte
# =========================================================
class ExpeditionCard(QFrame):

    def __init__(
        self,
        char_name,
        location,
        total_seconds,
        end_timestamp=None,
        on_delete=None,
        parent=None,
    ):
        super().__init__(parent)
        self.char_name = char_name
        self.total_seconds = total_seconds
        self.end_timestamp = (
            end_timestamp if end_timestamp else (time.time() + total_seconds)
        )
        self.on_delete_callback = on_delete
        self.notified = False

        self.setup_ui(char_name, location)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(shadow)

        self.style_card(active=True)

    def setup_ui(self, char_name, location):
        card_layout = QVBoxLayout(self)
        card_layout.setContentsMargins(15, 12, 15, 12)

        # Header
        header_layout = QHBoxLayout()

        self.lbl_avatar = QLabel()
        self.lbl_avatar.setFixedSize(40, 40)
        self.lbl_avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Bildpfad basierend auf dem Charakternamen zusammensetzen (z. B. "hu_tao.png")
        img_slug = char_name.lower().replace(" ", "_") + ".png"
        img_path = os.path.join(ASSETS_DIR, img_slug)

        if os.path.exists(img_path):
            pixmap = QPixmap(img_path).scaled(
                40, 40,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            self.lbl_avatar.setPixmap(pixmap)
            self.lbl_avatar.setStyleSheet("""
                border-radius: 20px;
                background-color: #3b3f54;
            """)
        else:
            # Fallback falls Grafik fehlt
            self.lbl_avatar.setText(char_name[0])
            self.lbl_avatar.setStyleSheet(f"""
                background-color: #3b3f54;
                color: {CORE_COLOR_CYAN};
                font-size: 18px;
                font-weight: bold;
                border-radius: 20px;
            """)

        header_layout.addWidget(self.lbl_avatar)

        text_v_layout = QVBoxLayout()
        lbl_name = QLabel(char_name)
        lbl_name.setStyleSheet("font-weight: bold; font-size: 13px; color: white;")
        self.lbl_loc = QLabel(location)
        self.lbl_loc.setStyleSheet("color: #aaaaaa; font-size: 11px;")
        text_v_layout.addWidget(lbl_name)
        text_v_layout.addWidget(self.lbl_loc)
        header_layout.addLayout(text_v_layout)

        header_layout.addStretch()

        # Löschen Button ("✕")
        btn_delete = QPushButton("✕")
        btn_delete.setFixedSize(24, 24)
        btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_delete.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #777;
                border: none;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                color: #ff5555;
                background-color: #38242a;
                border-radius: 12px;
            }
        """)
        btn_delete.clicked.connect(self.delete_click)
        header_layout.addWidget(btn_delete)

        card_layout.addLayout(header_layout)

        # Ring-Timer
        self.ring_timer = CircularProgressTimer(self)
        card_layout.addWidget(
            self.ring_timer, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Action-Button
        self.btn_action = QPushButton("Running")
        self.btn_action.setCursor(Qt.CursorShape.PointingHandCursor)
        card_layout.addWidget(self.btn_action)

        self.update_time()

    def delete_click(self):
        if self.on_delete_callback:
            self.on_delete_callback(self)

    def style_card(self, active=False):
        color = CORE_COLOR_CYAN if active else CORE_COLOR_AMBER
        self.setStyleSheet(f"""
            ExpeditionCard {{
                background-color: {CARD_BG_COLOR};
                border-radius: 12px;
                border: 1px solid #333847;
            }}
            QPushButton {{
                background-color: #2e323f;
                border: 1px solid {color};
                color: {color};
                border-radius: 6px;
                padding: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {color};
                color: {BG_COLOR_DARK};
            }}
        """)

    def get_remaining_seconds(self):
        return int(self.end_timestamp - time.time())

    def update_time(self):
        rem = self.get_remaining_seconds()
        self.ring_timer.set_time(rem, self.total_seconds)

        if rem <= 0:
            self.btn_action.setText("Claim Reward")
            self.style_card(active=False)
            if not self.notified:
                self.notified = True
                return True  # Löst Benachrichtigung aus
        return False

    def to_dict(self):
        return {
            "char_name": self.char_name,
            "location": self.lbl_loc.text(),
            "total_seconds": self.total_seconds,
            "end_timestamp": self.end_timestamp,
        }


# =========================================================
# Inline Overlay-Dialog
# =========================================================
class InlineAddDialog(QFrame):

    def __init__(self, parent=None, on_submit=None, on_cancel=None):
        super().__init__(parent)
        self.on_submit_callback = on_submit
        self.on_cancel_callback = on_cancel

        self.setFixedSize(380, 260)
        self.setStyleSheet(f"""
            InlineAddDialog {{
                background-color: {CARD_BG_COLOR};
                border: 2px solid {CORE_COLOR_CYAN};
                border-radius: 12px;
            }}
            QLabel {{ color: #e6e6e6; font-weight: bold; font-size: 12px; }}
            QComboBox, QLineEdit {{
                background-color: #1a1c24;
                color: white;
                border: 1px solid #3d4254;
                border-radius: 5px;
                padding: 5px 8px;
                font-size: 12px;
            }}
            QComboBox:focus, QLineEdit:focus {{ border: 1px solid {CORE_COLOR_CYAN}; }}
            QPushButton {{
                background-color: #2e323f;
                color: white;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: #3b3f54; }}
            QPushButton[primary="true"] {{
                background-color: {CORE_COLOR_CYAN};
                color: #1a1c24;
                border: none;
            }}
            QPushButton[primary="true"]:hover {{ background-color: #5effff; }}
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)

        lbl_title = QLabel("Neue Erkundung")
        lbl_title.setStyleSheet(
            f"font-size: 14px; color: {CORE_COLOR_CYAN}; margin-bottom: 5px;"
        )
        layout.addWidget(lbl_title)

        form_layout = QFormLayout()
        form_layout.setSpacing(8)

        self.combo_char = QComboBox()
        self.combo_char.addItems(sorted(CHARACTERS.keys()))
        self.combo_char.currentTextChanged.connect(self.on_char_changed)
        form_layout.addRow("Charakter:", self.combo_char)

        self.combo_region = QComboBox()
        self.combo_region.addItems(REGIONS)
        form_layout.addRow("Zielgebiet:", self.combo_region)

        self.input_detail = QLineEdit()
        self.input_detail.setPlaceholderText("Erz, Mora...")
        form_layout.addRow("Ressource:", self.input_detail)

        self.combo_duration = QComboBox()
        self.combo_duration.addItems([
            "4 Stunden",
            "8 Stunden",
            "12 Stunden",
            "16 Stunden (Bonus)",
            "20 Stunden (Standard)",
        ])
        form_layout.addRow("Dauer:", self.combo_duration)

        layout.addLayout(form_layout)
        layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_cancel = QPushButton("Abbrechen")
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel.clicked.connect(self.cancel_click)

        btn_start = QPushButton("Starten")
        btn_start.setProperty("primary", "true")
        btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_start.clicked.connect(self.submit_click)

        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_start)

        layout.addLayout(btn_layout)

        # Initialen Bonus-Status für den ersten Charakter in der Liste prüfen
        self.on_char_changed(self.combo_char.currentText())

    def on_char_changed(self, char_name):
        has_bonus = CHARACTERS.get(char_name, False)
        if has_bonus:
            self.combo_duration.setCurrentIndex(3)
        else:
            self.combo_duration.setCurrentIndex(4)

    def submit_click(self):
        duration_text = self.combo_duration.currentText()
        hours = int(duration_text.split()[0])
        region = self.combo_region.currentText()
        detail = self.input_detail.text().strip()
        location = f"{region} ({detail})" if detail else region

        if self.on_submit_callback:
            self.on_submit_callback(self.combo_char.currentText(), location, hours)

    def cancel_click(self):
        if self.on_cancel_callback:
            self.on_cancel_callback()


# =========================================================
# Hauptfenster
# =========================================================
class GenshinTrackerWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Genshin Impact Expedition Tracker")
        self.resize(1000, 700)

        self.setStyleSheet(f"""
            QMainWindow {{ background-color: {BG_COLOR_DARK}; }}
            QWidget {{ color: #e6e6e6; font-family: 'Segoe UI', sans-serif; }}
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        header_layout = QHBoxLayout()
        lbl_title = QLabel("Active Expeditions")
        lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        header_layout.addWidget(lbl_title)
        header_layout.addStretch()
        self.main_layout.addLayout(header_layout)

        btn_start_new = QPushButton("+ Start New Expedition")
        btn_start_new.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_start_new.setStyleSheet(f"""
            QPushButton {{
                background-color: #252833;
                border: 2px dashed #444;
                border-radius: 8px;
                padding: 15px;
                font-size: 14px;
                font-weight: bold;
                color: #888;
            }}
            QPushButton:hover {{
                border-color: {CORE_COLOR_CYAN};
                color: {CORE_COLOR_CYAN};
                background-color: #2a2e3a;
            }}
        """)
        btn_start_new.clicked.connect(self.open_add_dialog)
        self.main_layout.addWidget(btn_start_new)
        self.main_layout.addSpacing(20)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")

        self.grid_widget = QWidget()
        self.cards_grid = QGridLayout(self.grid_widget)
        self.cards_grid.setSpacing(20)

        scroll.setWidget(self.grid_widget)
        self.main_layout.addWidget(scroll)

        self.active_cards = []
        self.overlay_dialog = None

        # Timer
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.on_timer_tick)
        self.update_timer.start(1000)

        # Lade gespeicherte Erkundungen aus expeditions.json
        self.load_expeditions()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.overlay_dialog and self.overlay_dialog.isVisible():
            self.position_overlay()

    def position_overlay(self):
        x = (self.width() - self.overlay_dialog.width()) // 2
        y = (self.height() - self.overlay_dialog.height()) // 2
        self.overlay_dialog.move(x, y)

    def open_add_dialog(self):
        if len(self.active_cards) >= 5 or self.overlay_dialog:
            return

        self.overlay_dialog = InlineAddDialog(
            parent=self.central_widget,
            on_submit=self.on_dialog_submit,
            on_cancel=self.close_overlay,
        )
        self.position_overlay()
        self.overlay_dialog.show()
        self.overlay_dialog.raise_()

    def on_dialog_submit(self, char, loc, hours):
        self.create_card(char, loc, hours * 3600)
        self.close_overlay()
        self.save_expeditions()

    def close_overlay(self):
        if self.overlay_dialog:
            self.overlay_dialog.deleteLater()
            self.overlay_dialog = None

    def create_card(self, char, loc, total_seconds, end_timestamp=None):
        card = ExpeditionCard(
            char,
            loc,
            total_seconds,
            end_timestamp=end_timestamp,
            on_delete=self.remove_card,
            parent=self,
        )
        self.active_cards.append(card)
        self.regrid_cards()

    def remove_card(self, card_to_remove):
        if card_to_remove in self.active_cards:
            self.cards_grid.removeWidget(card_to_remove)
            self.active_cards.remove(card_to_remove)
            card_to_remove.deleteLater()
            self.regrid_cards()
            self.save_expeditions()

    def regrid_cards(self):
        for i, card in enumerate(self.active_cards):
            row = i // 3
            col = i % 3
            self.cards_grid.addWidget(card, row, col)

    def on_timer_tick(self):
        for card in self.active_cards:
            just_finished = card.update_time()
            if just_finished and notification:
                notification.notify(
                    title="Genshin Impact Tracker",
                    message=f"Die Erkundung von {card.char_name} ist abgeschlossen!",
                    app_name="GenshinTimer",
                    timeout=5,
                )

    # --- JSON Speicher- & Ladelogik ---
    def save_expeditions(self):
        data = [card.to_dict() for card in self.active_cards]
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Fehler beim Speichern: {e}")

    def load_expeditions(self):
        if not os.path.exists(SAVE_FILE):
            return
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    self.create_card(
                        item["char_name"],
                        item["location"],
                        item["total_seconds"],
                        end_timestamp=item["end_timestamp"],
                    )
        except Exception as e:
            print(f"Fehler beim Laden: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GenshinTrackerWindow()
    window.show()
    sys.exit(app.exec())
