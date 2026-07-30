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
    QLabel,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

# --- Pfade & Standardfarben ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "characters")
SAVE_FILE = os.path.join(BASE_DIR, "expeditions.json")

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

# Aktuell aktive Farb-Variablen
CORE_COLOR_CYAN = REGION_THEMES["Mondstadt (Anemo)"]["cyan"]
CORE_COLOR_AMBER = REGION_THEMES["Mondstadt (Anemo)"]["amber"]
BG_COLOR_DARK = REGION_THEMES["Mondstadt (Anemo)"]["bg_dark"]
CARD_BG_COLOR = REGION_THEMES["Mondstadt (Anemo)"]["card_bg"]

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
        self.is_active = True

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
        self.lbl_loc.setStyleSheet(f"""
            QLabel {{
                background-color: rgba(26, 28, 36, 220);
                color: {CORE_COLOR_CYAN};
                border: 1px solid #3d4254;
                border-radius: 8px;
                padding: 4px 10px;
                font-size: 11px;
                font-weight: bold;
            }}
        """)
        card_layout.addWidget(self.lbl_loc)

        self.btn_action = QPushButton("Running")
        self.btn_action.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_action.clicked.connect(self.on_action_click)
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

        self.lbl_loc.setStyleSheet(f"""
            QLabel {{
                background-color: rgba(26, 28, 36, 220);
                color: {CORE_COLOR_CYAN};
                border: 1px solid #3d4254;
                border-radius: 8px;
                padding: 4px 10px;
                font-size: 11px;
                font-weight: bold;
            }}
        """)

    def get_remaining_seconds(self):
        return int(self.end_timestamp - time.time())

    def update_time(self):
        rem = self.get_remaining_seconds()
        self.ring_timer.set_time(rem, self.total_seconds)

        if rem <= 0:
            self.btn_action.setText("Claim Reward")
            if self.is_active:
                self.is_active = False
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
        super().__init__()
        self.parent_window = parent_window
        self.current_resin = 120
        self.max_resin = 200
        self.last_resin_update = time.time()

        self.setObjectName("operations_hq_card")
        self.apply_theme_style()

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 90))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(6)

        self.lbl_header = QLabel("OPERATIONS HQ")
        self.lbl_header.setStyleSheet(
            f"font-weight: bold; font-size: 13px; color: {CORE_COLOR_CYAN}; letter-spacing: 1px;"
        )
        layout.addWidget(self.lbl_header)

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
        self.btn_edit_resin = QPushButton("⚙")
        self.btn_edit_resin.setFixedSize(16, 16)
        self.btn_edit_resin.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_edit_resin.setStyleSheet(f"""
            QPushButton {{
                background: transparent; border: none; color: #aaa; font-size: 10px; padding: 0;
            }}
            QPushButton:hover {{ color: {CORE_COLOR_CYAN}; }}
        """)
        self.btn_edit_resin.clicked.connect(self.edit_resin)
        h_resin_hdr.addWidget(lbl_resin_title)
        h_resin_hdr.addStretch()
        h_resin_hdr.addWidget(self.btn_edit_resin)

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

    def apply_theme_style(self):
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
        if hasattr(self, "lbl_header"):
            self.lbl_header.setStyleSheet(
                f"font-weight: bold; font-size: 13px; color: {CORE_COLOR_CYAN}; letter-spacing: 1px;"
            )
        if hasattr(self, "btn_edit_resin"):
            self.btn_edit_resin.setStyleSheet(f"""
                QPushButton {{
                    background: transparent; border: none; color: #aaa; font-size: 10px; padding: 0;
                }}
                QPushButton:hover {{ color: {CORE_COLOR_CYAN}; }}
            """)

    def edit_resin(self):
        if self.parent_window:
            self.parent_window.open_resin_dialog()

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
# Inline Overlay-Dialog: Expedition hinzufügen
# =========================================================
class InlineAddDialog(QFrame):

    DURATIONS_STANDARD = [
        ("4 Hours", 4),
        ("8 Hours", 8),
        ("12 Hours", 12),
        ("20 Hours (Standard)", 20),
    ]

    DURATIONS_BONUS = [
        ("3 Hours (Bonus 4h)", 3),
        ("6 Hours (Bonus 8h)", 6),
        ("9 Hours (Bonus 12h)", 9),
        ("15 Hours (Bonus 20h)", 15),
    ]

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
            QPushButton[primary="true"]:hover {{ background-color: {CORE_COLOR_CYAN}; }}
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
        self.combo_char.addItems(sorted(CHARACTERS))
        form_layout.addRow("Character:", self.combo_char)

        self.combo_region = QComboBox()
        self.combo_region.addItems(REGIONS)
        form_layout.addRow("Region:", self.combo_region)

        self.combo_resource = QComboBox()
        self.combo_resource.addItems(RESOURCES)
        form_layout.addRow("Resource:", self.combo_resource)

        self.combo_duration = QComboBox()
        form_layout.addRow("Duration:", self.combo_duration)

        self.combo_char.currentTextChanged.connect(self.update_bonus_state)
        self.combo_region.currentTextChanged.connect(self.update_bonus_state)

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

        self.update_bonus_state()

    def update_bonus_state(self):
        selected_char = self.combo_char.currentText()
        selected_region = self.combo_region.currentText()

        bonus_region = TIME_REDUCTION_BONUS.get(selected_char)
        has_bonus = (bonus_region is not None and bonus_region == selected_region)

        self.combo_duration.blockSignals(True)
        self.combo_duration.clear()

        options = self.DURATIONS_BONUS if has_bonus else self.DURATIONS_STANDARD
        for label, hours in options:
            self.combo_duration.addItem(label, userData=hours)

        self.combo_duration.setCurrentIndex(len(options) - 1)
        self.combo_duration.blockSignals(False)

    def submit_click(self):
        hours = self.combo_duration.currentData()
        if hours is None:
            hours = int(self.combo_duration.currentText().split()[0])

        region = self.combo_region.currentText()
        detail = self.combo_resource.currentText().strip()
        location = f"{region} ({detail})" if detail else region

        if self.on_submit_callback:
            self.on_submit_callback(self.combo_char.currentText(), location, hours)

    def cancel_click(self):
        if self.on_cancel_callback:
            self.on_cancel_callback()


# =========================================================
# Inline Overlay-Dialog: Resin anpassen
# =========================================================
class InlineResinDialog(QFrame):

    def __init__(self, current_resin=120, max_resin=200, on_submit=None, on_cancel=None, parent=None):
        super().__init__(parent)
        self.on_submit_callback = on_submit
        self.on_cancel_callback = on_cancel
        self.max_resin = max_resin

        self.setFixedSize(320, 180)
        self.setStyleSheet(f"""
            InlineResinDialog {{
                background-color: {CARD_BG_COLOR};
                border: 2px solid {CORE_COLOR_CYAN};
                border-radius: 12px;
            }}
            QLabel {{ color: #e6e6e6; font-weight: bold; font-size: 12px; }}
            QSpinBox {{
                background-color: #1a1c24;
                color: white;
                border: 1px solid #3d4254;
                border-radius: 5px;
                padding: 5px 8px;
                font-size: 14px;
                font-weight: bold;
            }}
            QSpinBox:focus {{ border: 1px solid {CORE_COLOR_CYAN}; }}
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
            QPushButton[primary="true"]:hover {{ background-color: {CORE_COLOR_CYAN}; }}
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)

        lbl_title = QLabel("Adjust Original Resin")
        lbl_title.setStyleSheet(f"font-size: 14px; color: {CORE_COLOR_CYAN}; margin-bottom: 5px;")
        layout.addWidget(lbl_title)

        form_layout = QFormLayout()
        form_layout.setSpacing(8)

        self.spin_resin = QSpinBox()
        self.spin_resin.setRange(0, self.max_resin)
        self.spin_resin.setValue(current_resin)
        form_layout.addRow("Current Resin:", self.spin_resin)

        layout.addLayout(form_layout)
        layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cancel.clicked.connect(self.cancel_click)

        btn_save = QPushButton("Save")
        btn_save.setProperty("primary", "true")
        btn_save.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_save.clicked.connect(self.submit_click)

        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_save)

        layout.addLayout(btn_layout)

    def submit_click(self):
        if self.on_submit_callback:
            self.on_submit_callback(self.spin_resin.value())

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

        self.current_theme_name = "Mondstadt (Anemo)"

        icon_path = os.path.join(ASSETS_DIR, "traveller.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(16, 16, 16, 16)

        # Header mit Title & Theme Chooser
        header_layout = QHBoxLayout()
        lbl_title = QLabel("Active Expeditions")
        lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        header_layout.addWidget(lbl_title)
        header_layout.addStretch()

        lbl_theme = QLabel("Theme:")
        lbl_theme.setStyleSheet("font-size: 12px; font-weight: bold; color: #aaa;")
        header_layout.addWidget(lbl_theme)

        self.combo_theme = QComboBox()
        self.combo_theme.addItems(list(REGION_THEMES.keys()))
        self.combo_theme.setCurrentText(self.current_theme_name)
        self.combo_theme.currentTextChanged.connect(self.apply_theme)
        header_layout.addWidget(self.combo_theme)

        self.main_layout.addLayout(header_layout)
        self.main_layout.addSpacing(10)

        # Cards Grid (nimmt den Hauptplatz ein)
        self.grid_widget = QWidget()
        self.cards_grid = QGridLayout(self.grid_widget)
        self.cards_grid.setContentsMargins(0, 0, 0, 0)
        self.cards_grid.setSpacing(12)

        for col in range(3):
            self.cards_grid.setColumnStretch(col, 1)
        for row in range(2):
            self.cards_grid.setRowStretch(row, 1)

        self.main_layout.addWidget(self.grid_widget, stretch=1)
        self.main_layout.addSpacing(10)

        # Start Button (ganz unten platziert)
        self.btn_start_new = QPushButton()
        self.btn_start_new.clicked.connect(self.open_add_dialog)
        self.main_layout.addWidget(self.btn_start_new)

        self.active_cards = []
        self.overlay_dialog = None

        self.hq_card = OperationsHQCard(parent_window=self)

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.on_timer_tick)
        self.update_timer.start(1000)

        self.load_expeditions()
        self.apply_theme(self.current_theme_name)
        self.update_add_button_state()

        self.setMinimumSize(1500, 975)
        self.resize(1500, 975)

    def apply_theme(self, theme_name):
        self.current_theme_name = theme_name
        theme = REGION_THEMES.get(theme_name, REGION_THEMES["Mondstadt (Anemo)"])

        global CORE_COLOR_CYAN, CORE_COLOR_AMBER, BG_COLOR_DARK, CARD_BG_COLOR
        CORE_COLOR_CYAN = theme["cyan"]
        CORE_COLOR_AMBER = theme["amber"]
        BG_COLOR_DARK = theme["bg_dark"]
        CARD_BG_COLOR = theme["card_bg"]

        self.setStyleSheet(f"""
            QMainWindow {{ background-color: {BG_COLOR_DARK}; }}
            QWidget {{ color: #e6e6e6; font-family: 'Segoe UI', sans-serif; }}
            QComboBox {{
                background-color: #1a1c24;
                color: white;
                border: 1px solid {CORE_COLOR_CYAN};
                border-radius: 5px;
                padding: 4px 8px;
                font-size: 12px;
            }}
        """)

        # HQ Card auffrischen
        if hasattr(self, "hq_card"):
            self.hq_card.apply_theme_style()
            self.hq_card.update_info()

        # Karten auffrischen
        for card in self.active_cards:
            card.style_card(active=card.get_remaining_seconds() > 0)
            card.ring_timer.update()

        self.update_add_button_state()
        self.save_expeditions()

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
                    background-color: {CARD_BG_COLOR};
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
        self.position_overlay()

    def position_overlay(self):
        if self.overlay_dialog:
            cw = self.central_widget
            x = (cw.width() - self.overlay_dialog.width()) // 2
            y = (cw.height() - self.overlay_dialog.height()) // 2
            self.overlay_dialog.move(max(0, x), max(0, y))

    def open_add_dialog(self):
        if len(self.active_cards) >= 5 or self.overlay_dialog:
            return

        self.overlay_dialog = InlineAddDialog(
            parent=self.central_widget,
            on_submit=self.on_dialog_submit,
            on_cancel=self.close_overlay,
        )
        self.overlay_dialog.show()
        self.overlay_dialog.raise_()
        self.position_overlay()

    def open_resin_dialog(self):
        if self.overlay_dialog:
            return

        self.overlay_dialog = InlineResinDialog(
            current_resin=self.hq_card.current_resin,
            max_resin=self.hq_card.max_resin,
            on_submit=self.on_resin_submit,
            on_cancel=self.close_overlay,
            parent=self.central_widget,
        )
        self.overlay_dialog.show()
        self.overlay_dialog.raise_()
        self.position_overlay()

    def on_dialog_submit(self, char, loc, hours):
        self.create_card(char, loc, hours * 3600)
        self.close_overlay()
        self.save_expeditions()

    def on_resin_submit(self, new_resin_val):
        self.hq_card.current_resin = new_resin_val
        self.hq_card.last_resin_update = time.time()
        self.hq_card.update_info()
        self.save_expeditions()
        self.close_overlay()

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
        data = {
            "expeditions": [card.to_dict() for card in self.active_cards],
            "resin": self.hq_card.current_resin,
            "last_resin_update": self.hq_card.last_resin_update,
            "theme": self.current_theme_name,
        }
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

                if isinstance(data, list):
                    expeditions = data
                else:
                    expeditions = data.get("expeditions", [])
                    self.hq_card.current_resin = data.get("resin", 120)
                    self.hq_card.last_resin_update = data.get("last_resin_update", time.time())
                    self.current_theme_name = data.get("theme", "Mondstadt (Anemo)")

                for item in expeditions:
                    self.create_card(
                        item["char_name"],
                        item["location"],
                        item["total_seconds"],
                        end_timestamp=item["end_timestamp"],
                    )
                if hasattr(self, "combo_theme"):
                    self.combo_theme.setCurrentText(self.current_theme_name)
        except Exception as e:
            print(f"Error loading: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GenshinTrackerWindow()
    window.show()
    sys.exit(app.exec())
