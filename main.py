import json
import os
import sys
import time
from datetime import datetime, timedelta

try:
    from plyer import notification
except ImportError:
    notification = None

from PyQt6.QtCore import QRectF, QSize, Qt, QTimer
from PyQt6.QtGui import QBrush, QColor, QFont, QIcon, QPainter, QPen
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QFrame,
    QGraphicsDropShadowEffect,
    QGridLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QMainWindow,
    QPushButton,
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

CHARACTERS = {
    "Albedo": False, "Alhaitham": False, "Aloy": False, "Amber": False,
    "Arataki Itto": False, "Arlecchino": False, "Barbara": False, "Beidou": False,
    "Bennett": True, "Candace": False, "Charlotte": False, "Chasca": False,
    "Chevreuse": False, "Chiori": False, "Chongyun": True, "Citlali": False,
    "Clorinde": False, "Collei": False, "Cyno": False, "Dehya": False,
    "Diluc": False, "Diona": False, "Dori": False, "Emilie": False,
    "Eula": False, "Faruzan": False, "Fischl": True, "Freminet": False,
    "Furina": False, "Gaming": False, "Ganyu": False, "Gorou": False,
    "Hu Tao": False, "Iansan": False, "Jean": False, "Kachina": False,
    "Kaedehara Kazuha": False, "Kaeya": False, "Kamisato Ayaka": False,
    "Kamisato Ayato": False, "Kaveh": False, "Keqing": True, "Kinich": False,
    "Kirara": False, "Klee": False, "Kujou Sara": False, "Kuki Shinobu": False,
    "Lan Yan": False, "Lanyan": False, "Layla": False, "Lisa": False,
    "Lynette": False, "Lyney": False, "Mavuika": False, "Mika": False,
    "Mona": False, "Mualani": False, "Nahida": False, "Navia": False,
    "Neuvillette": False, "Nilou": False, "Ningguang": False, "Noelle": False,
    "Ororon": False, "Qiqi": False, "Raiden Shogun": False, "Razor": False,
    "Rosaria": False, "Sangonomiya Kokomi": False, "Sayu": False, "Sethos": False,
    "Shenhe": True, "Shikanoin Heizou": False, "Sigewinne": False, "Sucrose": False,
    "Thoma": False, "Tighnari": False, "Traveller": False, "Venti": False,
    "Wanderer": False, "Wriothesley": False, "Xiangling": False, "Xianyun": False,
    "Xiao": False, "Xilonen": False, "Xingqiu": False, "Xinyan": False,
    "Yae Miko": False, "Yanfei": False, "Yao Yao": False, "Yelan": False,
    "Yoimiya": False, "Yun Jin": False, "Zhongli": False,
}

REGIONS = ["Mondstadt", "Liyue", "Inazuma", "Sumeru", "Fontaine", "Natlan"]
RESOURCES = [
    "Mora",
    "Ores (Iron & Crystal)",
    "Meat & Fowl",
    "Ingredients & Plants",
    "Fish",
]


# =========================================================
# Custom Widget: Ring-Timer
# =========================================================
class CircularProgressTimer(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(120, 120)
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

        painter.setBrush(QBrush(QColor(18, 20, 28, 220)))
        bg_pen = QPen(QColor("#1a1c24"), pen_width)
        bg_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(bg_pen)
        painter.drawEllipse(rect)

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

        painter.setPen(color)
        font = QFont("Segoe UI", 12, QFont.Weight.Bold)
        painter.setFont(font)

        if self.is_complete:
            time_str = "READY!"
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

        self.setObjectName("expedition_card_widget")

        card_layout = QVBoxLayout(self)
        card_layout.setContentsMargins(15, 12, 15, 12)
        card_layout.setSpacing(6)

        header_layout = QHBoxLayout()
        lbl_name = QLabel(char_name)
        lbl_name.setStyleSheet("font-weight: bold; font-size: 14px; color: white;")
        header_layout.addWidget(lbl_name)
        header_layout.addStretch()

        btn_delete = QPushButton("✕")
        btn_delete.setFixedSize(24, 24)
        btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_delete.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #aaa;
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

        self.ring_timer = CircularProgressTimer(self)
        card_layout.addWidget(
            self.ring_timer, alignment=Qt.AlignmentFlag.AlignCenter
        )

        card_layout.addStretch()

        self.lbl_loc = QLabel(f"📍 {location}")
        self.lbl_loc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_loc.setStyleSheet("""
            QLabel {
                background-color: rgba(26, 28, 36, 220);
                color: #38e3e3;
                border: 1px solid #3d4254;
                border-radius: 8px;
                padding: 4px 10px;
                font-size: 11px;
                font-weight: bold;
            }
        """)
        card_layout.addWidget(self.lbl_loc)

        self.btn_action = QPushButton("Running")
        self.btn_action.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_action.clicked.connect(self.on_action_click)  # Nur ausführen, wenn "Claim Reward"
        card_layout.addWidget(self.btn_action)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 90))
        self.setGraphicsEffect(shadow)

        self.style_card(active=True)
        self.update_time()

    def on_action_click(self):
        # Nur auflösen, wenn die Expedition beendet ist ("Claim Reward")
        if self.get_remaining_seconds() <= 0:
            self.delete_click()

    def delete_click(self):
        if self.on_delete_callback:
            self.on_delete_callback(self)

    def style_card(self, active=False):
        color = CORE_COLOR_CYAN if active else CORE_COLOR_AMBER

        img_slug = self.char_name.lower().replace(" ", "_") + ".png"
        img_path = os.path.join(ASSETS_DIR, img_slug).replace("\\", "/")

        if os.path.exists(img_path):
            bg_style = f"""
                background-image: url("{img_path}");
                background-repeat: no-repeat;
                background-position: center center;
                background-color: qradialgradient(
                    cx:0.5, cy:0.5, radius: 0.8,
                    fx:0.5, fy:0.5,
                    stop:0 rgba(18, 20, 28, 200),
                    stop:0.6 rgba(20, 22, 30, 230),
                    stop:1 rgba(26, 28, 36, 255)
                );
            """
        else:
            bg_style = f"background-color: {CARD_BG_COLOR};"

        self.setStyleSheet(f"""
            QFrame#expedition_card_widget {{
                {bg_style}
                border-radius: 12px;
                border: 1px solid #333847;
            }}
            QPushButton {{
                background-color: rgba(46, 50, 63, 220);
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
                return True
        else:
            self.btn_action.setText("Running")
        return False

    def to_dict(self):
        clean_loc = self.lbl_loc.text().replace("📍 ", "")
        return {
            "char_name": self.char_name,
            "location": clean_loc,
            "total_seconds": self.total_seconds,
            "end_timestamp": self.end_timestamp,
        }


# =========================================================
# Custom Widget: Operations HQ
# =========================================================
class OperationsHQCard(QFrame):

    def __init__(self, parent_window=None):
        super().__init__(parent_window)
        self.parent_window = parent_window
        self.current_resin = 120
        self.max_resin = 200
        self.last_resin_update = time.time()

        self.setObjectName("operations_hq_card")
        self.setStyleSheet(f"""
            QFrame#operations_hq_card {{
                background-color: {CARD_BG_COLOR};
                border-radius: 12px;
                border: 1px solid #333847;
            }}
            QLabel {{ color: #e6e6e6; }}
            QPushButton {{
                background-color: #2e323f;
                border: 1px solid {CORE_COLOR_CYAN};
                color: {CORE_COLOR_CYAN};
                border-radius: 6px;
                padding: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {CORE_COLOR_CYAN};
                color: {BG_COLOR_DARK};
            }}
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 90))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(6)

        lbl_header = QLabel("OPERATIONS HQ")
        lbl_header.setStyleSheet(
            f"font-weight: bold; font-size: 13px; color: {CORE_COLOR_CYAN}; letter-spacing: 1px;"
        )
        layout.addWidget(lbl_header)

        # Box 1: Next Ready
        box_next = QFrame()
        box_next.setStyleSheet("background-color: #1a1c24; border-radius: 6px;")
        v_next = QVBoxLayout(box_next)
        v_next.setSpacing(2)
        v_next.setContentsMargins(10, 6, 10, 6)

        lbl_next_title = QLabel("NEXT ARRIVAL")
        lbl_next_title.setStyleSheet("font-size: 9px; color: #888; font-weight: bold;")
        self.lbl_next_val = QLabel("No active expeditions")
        self.lbl_next_val.setStyleSheet(f"font-size: 11px; font-weight: bold; color: {CORE_COLOR_AMBER};")

        v_next.addWidget(lbl_next_title)
        v_next.addWidget(self.lbl_next_val)
        layout.addWidget(box_next)

        # Box 2: Server Reset
        box_reset = QFrame()
        box_reset.setStyleSheet("background-color: #1a1c24; border-radius: 6px;")
        v_reset = QVBoxLayout(box_reset)
        v_reset.setSpacing(2)
        v_reset.setContentsMargins(10, 6, 10, 6)

        lbl_reset_title = QLabel("DAILY RESET (04:00)")
        lbl_reset_title.setStyleSheet("font-size: 9px; color: #888; font-weight: bold;")
        self.lbl_reset_val = QLabel("00h 00m")
        self.lbl_reset_val.setStyleSheet("font-size: 11px; font-weight: bold; color: white;")

        v_reset.addWidget(lbl_reset_title)
        v_reset.addWidget(self.lbl_reset_val)
        layout.addWidget(box_reset)

        # Box 3: Resin Tracker
        box_resin = QFrame()
        box_resin.setStyleSheet("background-color: #1a1c24; border-radius: 6px;")
        v_resin = QVBoxLayout(box_resin)
        v_resin.setSpacing(2)
        v_resin.setContentsMargins(10, 6, 10, 6)

        h_resin_hdr = QHBoxLayout()
        lbl_resin_title = QLabel("RESIN COUNTER")
        lbl_resin_title.setStyleSheet("font-size: 9px; color: #888; font-weight: bold;")
        btn_edit_resin = QPushButton("⚙")
        btn_edit_resin.setFixedSize(16, 16)
        btn_edit_resin.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_edit_resin.setStyleSheet("""
            QPushButton {
                background: transparent; border: none; color: #aaa; font-size: 10px; padding: 0;
            }
            QPushButton:hover { color: #38e3e3; }
        """)
        btn_edit_resin.clicked.connect(self.edit_resin)
        h_resin_hdr.addWidget(lbl_resin_title)
        h_resin_hdr.addStretch()
        h_resin_hdr.addWidget(btn_edit_resin)

        self.lbl_resin_val = QLabel("120 / 200")
        self.lbl_resin_val.setStyleSheet("font-size: 10px; font-weight: bold; color: white;")

        v_resin.addLayout(h_resin_hdr)
        v_resin.addWidget(self.lbl_resin_val)
        layout.addWidget(box_resin)

        layout.addStretch()

        self.btn_claim_all = QPushButton("Claim All Ready")
        self.btn_claim_all.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_claim_all.clicked.connect(self.claim_all)
        layout.addWidget(self.btn_claim_all)

        self.update_info()

    def edit_resin(self):
        val, ok = QInputDialog.getInt(
            self, "Adjust Resin", f"Current Resin (0-{self.max_resin}):", self.current_resin, 0, self.max_resin
        )
        if ok:
            self.current_resin = val
            self.last_resin_update = time.time()
            self.update_info()

    def claim_all(self):
        if not self.parent_window:
            return
        ready_cards = [card for card in self.parent_window.active_cards if card.get_remaining_seconds() <= 0]
        for card in ready_cards:
            self.parent_window.remove_card(card)

    def update_info(self):
        now = time.time()
        elapsed = int(now - self.last_resin_update)
        gained = elapsed // 480
        if gained > 0 and self.current_resin < self.max_resin:
            self.current_resin = min(self.max_resin, self.current_resin + gained)
            self.last_resin_update += gained * 480

        if self.current_resin >= self.max_resin:
            self.lbl_resin_val.setText(f"{self.max_resin} / {self.max_resin} (FULL!)")
            self.lbl_resin_val.setStyleSheet(f"font-size: 10px; font-weight: bold; color: {CORE_COLOR_AMBER};")
        else:
            needed_resin = self.max_resin - self.current_resin
            seconds_left = (needed_resin * 480) - (int(now - self.last_resin_update) % 480)
            h = seconds_left // 3600
            m = (seconds_left % 3600) // 60
            self.lbl_resin_val.setText(f"{self.current_resin} / {self.max_resin} (Full in {h:02d}h {m:02d}m)")
            self.lbl_resin_val.setStyleSheet("font-size: 10px; font-weight: bold; color: white;")

        dt_now = datetime.now()
        dt_reset = dt_now.replace(hour=4, minute=0, second=0, microsecond=0)
        if dt_now >= dt_reset:
            dt_reset += timedelta(days=1)
        time_to_reset = dt_reset - dt_now
        res_h = int(time_to_reset.total_seconds() // 3600)
        res_m = int((time_to_reset.total_seconds() % 3600) // 60)
        self.lbl_reset_val.setText(f"In {res_h:02d}h {res_m:02d}m")

        if self.parent_window and self.parent_window.active_cards:
            active = self.parent_window.active_cards
            ready_cards = [c for c in active if c.get_remaining_seconds() <= 0]
            if ready_cards:
                self.lbl_next_val.setText(f"{len(ready_cards)} Ready to claim!")
                self.lbl_next_val.setStyleSheet(f"font-size: 11px; font-weight: bold; color: {CORE_COLOR_AMBER};")
            else:
                next_card = min(active, key=lambda c: c.get_remaining_seconds())
                rem = next_card.get_remaining_seconds()
                h = rem // 3600
                m = (rem % 3600) // 60
                s = rem % 60
                self.lbl_next_val.setText(f"{next_card.char_name} in {h:02d}:{m:02d}:{s:02d}")
                self.lbl_next_val.setStyleSheet(f"font-size: 11px; font-weight: bold; color: {CORE_COLOR_CYAN};")
        else:
            self.lbl_next_val.setText("No active expeditions")
            self.lbl_next_val.setStyleSheet("font-size: 11px; font-weight: bold; color: #888;")


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
            QComboBox {{
                background-color: #1a1c24;
                color: white;
                border: 1px solid #3d4254;
                border-radius: 5px;
                padding: 5px 8px;
                font-size: 12px;
            }}
            QComboBox:focus {{ border: 1px solid {CORE_COLOR_CYAN}; }}
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

        lbl_title = QLabel("New Expedition")
        lbl_title.setStyleSheet(
            f"font-size: 14px; color: {CORE_COLOR_CYAN}; margin-bottom: 5px;"
        )
        layout.addWidget(lbl_title)

        form_layout = QFormLayout()
        form_layout.setSpacing(8)

        self.combo_char = QComboBox()
        self.combo_char.addItems(sorted(CHARACTERS.keys()))
        self.combo_char.currentTextChanged.connect(self.on_char_changed)
        form_layout.addRow("Character:", self.combo_char)

        self.combo_region = QComboBox()
        self.combo_region.addItems(REGIONS)
        form_layout.addRow("Region:", self.combo_region)

        self.combo_resource = QComboBox()
        self.combo_resource.addItems(RESOURCES)
        form_layout.addRow("Resource:", self.combo_resource)

        self.combo_duration = QComboBox()
        self.combo_duration.addItems([
            "4 Hours",
            "8 Hours",
            "12 Hours",
            "16 Hours (Bonus)",
            "20 Hours (Standard)",
        ])
        form_layout.addRow("Duration:", self.combo_duration)

        layout.addLayout(form_layout)
        layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel.clicked.connect(self.cancel_click)

        btn_start = QPushButton("Start")
        btn_start.setProperty("primary", "true")
        btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_start.clicked.connect(self.submit_click)

        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_start)

        layout.addLayout(btn_layout)

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
        detail = self.combo_resource.currentText().strip()
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

        icon_path = os.path.join(ASSETS_DIR, "traveller.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.setStyleSheet(f"""
            QMainWindow {{ background-color: {BG_COLOR_DARK}; }}
            QWidget {{ color: #e6e6e6; font-family: 'Segoe UI', sans-serif; }}
        """)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(16, 16, 16, 16)

        header_layout = QHBoxLayout()
        lbl_title = QLabel("Active Expeditions")
        lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        header_layout.addWidget(lbl_title)
        header_layout.addStretch()
        self.main_layout.addLayout(header_layout)

        self.btn_start_new = QPushButton()
        self.btn_start_new.clicked.connect(self.open_add_dialog)
        self.main_layout.addWidget(self.btn_start_new)
        self.main_layout.addSpacing(10)

        self.grid_widget = QWidget()
        self.cards_grid = QGridLayout(self.grid_widget)
        self.cards_grid.setContentsMargins(0, 0, 0, 0)
        self.cards_grid.setSpacing(12)

        for col in range(3):
            self.cards_grid.setColumnStretch(col, 1)
        for row in range(2):
            self.cards_grid.setRowStretch(row, 1)

        self.main_layout.addWidget(self.grid_widget, stretch=1)

        self.active_cards = []
        self.overlay_dialog = None

        self.hq_card = OperationsHQCard(parent_window=self)

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.on_timer_tick)
        self.update_timer.start(1000)

        self.load_expeditions()
        self.update_add_button_state()

        self.setMinimumSize(1500, 975)
        self.resize(1500, 975)

    def update_add_button_state(self):
        count = len(self.active_cards)
        max_limit = 5

        if count >= max_limit:
            self.btn_start_new.setEnabled(False)
            self.btn_start_new.setText(f"Limit Reached ({count}/{max_limit} Expeditions)")
            self.btn_start_new.setCursor(Qt.CursorShape.ForbiddenCursor)
            self.btn_start_new.setStyleSheet("""
                QPushButton {
                    background-color: #1e2029;
                    border: 2px dashed #333745;
                    border-radius: 8px;
                    padding: 10px;
                    font-size: 13px;
                    font-weight: bold;
                    color: #555866;
                }
            """)
        else:
            self.btn_start_new.setEnabled(True)
            self.btn_start_new.setText(f"+ Start New Expedition ({count}/{max_limit})")
            self.btn_start_new.setCursor(Qt.CursorShape.PointingHandCursor)
            self.btn_start_new.setStyleSheet(f"""
                QPushButton {{
                    background-color: #252833;
                    border: 2px dashed #444;
                    border-radius: 8px;
                    padding: 10px;
                    font-size: 13px;
                    font-weight: bold;
                    color: #888;
                }}
                QPushButton:hover {{
                    border-color: {CORE_COLOR_CYAN};
                    color: {CORE_COLOR_CYAN};
                    background-color: #2a2e3a;
                }}
            """)

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
        for i in reversed(range(self.cards_grid.count())):
            widget = self.cards_grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for i, card in enumerate(self.active_cards):
            row = i // 3
            col = i % 3
            self.cards_grid.addWidget(card, row, col)

        hq_index = len(self.active_cards)
        hq_row = hq_index // 3
        hq_col = hq_index % 3
        self.cards_grid.addWidget(self.hq_card, hq_row, hq_col)

        self.update_add_button_state()
        self.hq_card.update_info()

    def on_timer_tick(self):
        for card in self.active_cards:
            just_finished = card.update_time()
            if just_finished and notification:
                notification.notify(
                    title="Genshin Impact Tracker",
                    message=f"The expedition of {card.char_name} has finished!",
                    app_name="GenshinTimer",
                    timeout=5,
                )
        self.hq_card.update_info()

    def save_expeditions(self):
        data = [card.to_dict() for card in self.active_cards]
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving: {e}")

    def load_expeditions(self):
        if not os.path.exists(SAVE_FILE):
            self.regrid_cards()
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
            print(f"Error loading: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GenshinTrackerWindow()
    window.show()
    sys.exit(app.exec())
