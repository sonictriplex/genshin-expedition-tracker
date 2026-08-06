import os
import time
from datetime import datetime, timedelta

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from config import ASSETS_DIR, get_theme
from translations import tr


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
        theme = get_theme()
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

        color = QColor(theme["amber"]) if self.is_complete else QColor(theme["cyan"])
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
            time_str = tr("ready")
        else:
            h = max(0, self.remaining_seconds) // 3600
            m = (max(0, self.remaining_seconds) % 3600) // 60
            s = max(0, self.remaining_seconds) % 60
            time_str = f"{h:02d}:{m:02d}:{s:02d}"

        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, time_str)


class ExpeditionCard(QFrame):
    def __init__(self, char_name, location, total_seconds, end_timestamp=None, on_delete=None, parent=None):
        super().__init__(parent)
        self.char_name = char_name
        self.total_seconds = total_seconds
        self.end_timestamp = end_timestamp if end_timestamp else (time.time() + total_seconds)
        self.on_delete_callback = on_delete
        self.parent_window = parent
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

        self.btn_edit = QPushButton("✏️")
        self.btn_edit.setFixedSize(24, 24)
        self.btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_edit.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #aaa;
                border: none;
                font-size: 12px;
            }
            QPushButton:hover {
                color: #55aaff;
                background-color: #263345;
                border-radius: 12px;
            }
        """)
        self.btn_edit.clicked.connect(self.open_edit_dialog)
        header_layout.addWidget(self.btn_edit)

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
        card_layout.addWidget(self.ring_timer, alignment=Qt.AlignmentFlag.AlignCenter)

        card_layout.addStretch()

        self.lbl_loc = QLabel(f"📍 {location}")
        self.lbl_loc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.lbl_loc)

        self.btn_action = QPushButton(tr("running"))
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

    def open_edit_dialog(self):
        if self.parent_window and hasattr(self.parent_window, "open_edit_timer_dialog"):
            self.parent_window.open_edit_timer_dialog(self)

    def on_action_click(self):
        if self.get_remaining_seconds() <= 0:
            self.delete_click()

    def delete_click(self):
        if self.on_delete_callback:
            self.on_delete_callback(self)

    def style_card(self, active=False):
        theme = get_theme()
        color = theme["cyan"] if active else theme["amber"]

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
            bg_style = f"background-color: {theme['card_bg']};"

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
                color: {theme['bg_dark']};
            }}
        """)

        self.lbl_loc.setStyleSheet(f"""
            QLabel {{
                background-color: rgba(26, 28, 36, 220);
                color: {theme['cyan']};
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
            self.btn_action.setText(tr("claim_reward"))
            if self.is_active:
                self.is_active = False
                self.style_card(active=False)

            if not self.notified:
                self.notified = True
                return True
        else:
            self.btn_action.setText(tr("running"))
        return False

    def to_dict(self):
        clean_loc = self.lbl_loc.text().replace("📍 ", "")
        return {
            "char_name": self.char_name,
            "location": clean_loc,
            "total_seconds": self.total_seconds,
            "end_timestamp": self.end_timestamp,
        }


class OperationsHQCard(QFrame):
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window
        self.current_resin = 120
        self.max_resin = 200
        self.last_resin_update = time.time()

        self.setObjectName("operations_hq_card")

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 90))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(6)

        self.lbl_header = QLabel()
        layout.addWidget(self.lbl_header)

        # Box 1: Next Ready
        box_next = QFrame()
        box_next.setStyleSheet("background-color: #1a1c24; border-radius: 6px;")
        v_next = QVBoxLayout(box_next)
        v_next.setSpacing(2)
        v_next.setContentsMargins(10, 6, 10, 6)

        self.lbl_next_title = QLabel()
        self.lbl_next_title.setStyleSheet("font-size: 9px; color: #888; font-weight: bold;")
        self.lbl_next_val = QLabel()

        v_next.addWidget(self.lbl_next_title)
        v_next.addWidget(self.lbl_next_val)
        layout.addWidget(box_next)

        # Box 2: Server Reset
        box_reset = QFrame()
        box_reset.setStyleSheet("background-color: #1a1c24; border-radius: 6px;")
        v_reset = QVBoxLayout(box_reset)
        v_reset.setSpacing(2)
        v_reset.setContentsMargins(10, 6, 10, 6)

        self.lbl_reset_title = QLabel()
        self.lbl_reset_title.setStyleSheet("font-size: 9px; color: #888; font-weight: bold;")
        self.lbl_reset_val = QLabel()
        self.lbl_reset_val.setStyleSheet("font-size: 11px; font-weight: bold; color: white;")

        v_reset.addWidget(self.lbl_reset_title)
        v_reset.addWidget(self.lbl_reset_val)
        layout.addWidget(box_reset)

        # Box 3: Resin Tracker
        box_resin = QFrame()
        box_resin.setStyleSheet("background-color: #1a1c24; border-radius: 6px;")
        v_resin = QVBoxLayout(box_resin)
        v_resin.setSpacing(2)
        v_resin.setContentsMargins(10, 6, 10, 6)

        h_resin_hdr = QHBoxLayout()
        self.lbl_resin_title = QLabel()
        self.lbl_resin_title.setStyleSheet("font-size: 9px; color: #888; font-weight: bold;")
        self.btn_edit_resin = QPushButton("⚙")
        self.btn_edit_resin.setFixedSize(16, 16)
        self.btn_edit_resin.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_edit_resin.clicked.connect(self.edit_resin)
        h_resin_hdr.addWidget(self.lbl_resin_title)
        h_resin_hdr.addStretch()
        h_resin_hdr.addWidget(self.btn_edit_resin)

        self.lbl_resin_val = QLabel()
        self.lbl_resin_val.setStyleSheet("font-size: 10px; font-weight: bold; color: white;")

        v_resin.addLayout(h_resin_hdr)
        v_resin.addWidget(self.lbl_resin_val)
        layout.addWidget(box_resin)

        layout.addStretch()

        self.btn_claim_all = QPushButton()
        self.btn_claim_all.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_claim_all.clicked.connect(self.claim_all)
        layout.addWidget(self.btn_claim_all)

        self.retranslate_ui()
        self.apply_theme_style()
        self.update_info()

    def retranslate_ui(self):
        """Aktualisiert alle UI-Texte dynamisch bei Sprachwechsel"""
        self.lbl_header.setText(tr("hq_title"))
        self.lbl_next_title.setText(tr("hq_next_title"))
        self.lbl_reset_title.setText(tr("hq_reset_title"))
        self.lbl_resin_title.setText(tr("hq_resin_title"))
        self.btn_claim_all.setText(tr("hq_claim_all"))
        self.update_info()

    def apply_theme_style(self):
        theme = get_theme()
        self.setStyleSheet(f"""
            QFrame#operations_hq_card {{
                background-color: {theme['card_bg']};
                border-radius: 12px;
                border: 1px solid #333847;
            }}
            QLabel {{ color: #e6e6e6; }}
            QPushButton {{
                background-color: #2e323f;
                border: 1px solid {theme['cyan']};
                color: {theme['cyan']};
                border-radius: 6px;
                padding: 6px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {theme['cyan']};
                color: {theme['bg_dark']};
            }}
        """)
        if hasattr(self, "lbl_header"):
            self.lbl_header.setStyleSheet(
                f"font-weight: bold; font-size: 13px; color: {theme['cyan']}; letter-spacing: 1px;"
            )
        if hasattr(self, "btn_edit_resin"):
            self.btn_edit_resin.setStyleSheet(f"""
                QPushButton {{
                    background: transparent; border: none; color: #aaa; font-size: 10px; padding: 0;
                }}
                QPushButton:hover {{ color: {theme['cyan']}; }}
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
        theme = get_theme()
        now = time.time()
        elapsed = int(now - self.last_resin_update)
        gained = elapsed // 480
        if gained > 0 and self.current_resin < self.max_resin:
            self.current_resin = min(self.max_resin, self.current_resin + gained)
            self.last_resin_update += gained * 480

        if self.current_resin >= self.max_resin:
            self.lbl_resin_val.setText(tr("hq_resin_full", max=self.max_resin))
            self.lbl_resin_val.setStyleSheet(f"font-size: 10px; font-weight: bold; color: {theme['amber']};")
        else:
            needed_resin = self.max_resin - self.current_resin
            seconds_left = (needed_resin * 480) - (int(now - self.last_resin_update) % 480)
            h = seconds_left // 3600
            m = (seconds_left % 3600) // 60
            self.lbl_resin_val.setText(tr("hq_resin_countdown", current=self.current_resin, max=self.max_resin, h=h, m=m))
            self.lbl_resin_val.setStyleSheet("font-size: 10px; font-weight: bold; color: white;")

        dt_now = datetime.now()
        dt_reset = dt_now.replace(hour=4, minute=0, second=0, microsecond=0)
        if dt_now >= dt_reset:
            dt_reset += timedelta(days=1)
        time_to_reset = dt_reset - dt_now
        res_h = int(time_to_reset.total_seconds() // 3600)
        res_m = int((time_to_reset.total_seconds() % 3600) // 60)
        self.lbl_reset_val.setText(tr("hq_reset_countdown", h=res_h, m=res_m))

        if self.parent_window and self.parent_window.active_cards:
            active = self.parent_window.active_cards
            ready_cards = [c for c in active if c.get_remaining_seconds() <= 0]
            if ready_cards:
                self.lbl_next_val.setText(tr("hq_ready_count", count=len(ready_cards)))
                self.lbl_next_val.setStyleSheet(f"font-size: 11px; font-weight: bold; color: {theme['amber']};")
            else:
                next_card = min(active, key=lambda c: c.get_remaining_seconds())
                rem = next_card.get_remaining_seconds()
                h = rem // 3600
                m = (rem % 3600) // 60
                s = rem % 60
                self.lbl_next_val.setText(tr("hq_next_in", char=next_card.char_name, h=h, m=m, s=s))
                self.lbl_next_val.setStyleSheet(f"font-size: 11px; font-weight: bold; color: {theme['cyan']};")
        else:
            self.lbl_next_val.setText(tr("hq_no_active"))
            self.lbl_next_val.setStyleSheet("font-size: 11px; font-weight: bold; color: #888;")