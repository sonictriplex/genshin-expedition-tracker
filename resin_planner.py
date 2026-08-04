import datetime
import math
import time
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QSpinBox,
    QVBoxLayout,
)
from config import get_theme
from translations import tr


class ResinPlannerWidget(QFrame):
    def __init__(self, parent_window=None):
        super().__init__(parent_window)
        self.parent_window = parent_window

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(14)
        main_layout.setContentsMargins(16, 16, 16, 16)

        # --- Header ---
        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        main_layout.addWidget(self.title_label)

        # --- Grid Layout for Input ---
        grid = QGridLayout()
        grid.setSpacing(12)

        self.lbl_current_resin = QLabel()
        self.lbl_current_resin.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        grid.addWidget(self.lbl_current_resin, 0, 0)

        self.spin_resin = QSpinBox()
        self.spin_resin.setRange(0, 200)
        self.spin_resin.setValue(120)
        self.spin_resin.valueChanged.connect(self.calculate)
        grid.addWidget(self.spin_resin, 0, 1)

        main_layout.addLayout(grid)

        # Progress Bar for Visualizing Cap Level
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 200)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFixedHeight(22)
        main_layout.addWidget(self.progress_bar)

        # --- Results Box ---
        self.results_card = QFrame()
        self.results_card.setObjectName("sub_card")
        v_res = QVBoxLayout(self.results_card)
        v_res.setContentsMargins(12, 12, 12, 12)
        v_res.setSpacing(8)

        self.lbl_res_title = QLabel()
        self.lbl_res_title.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        v_res.addWidget(self.lbl_res_title)

        self.lbl_time_to_full = QLabel()
        self.lbl_cap_timestamp = QLabel()
        self.lbl_warning_time = QLabel()

        v_res.addWidget(self.lbl_time_to_full)
        v_res.addWidget(self.lbl_cap_timestamp)
        v_res.addWidget(self.lbl_warning_time)

        main_layout.addWidget(self.results_card)
        main_layout.addStretch()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.calculate)
        self.timer.start(10000)  # Refresh every 10 seconds

        self.retranslate_ui()
        self.apply_theme_style()
        self.calculate()

    def retranslate_ui(self):
        """Aktualisiert alle UI-Texte dynamisch bei Sprachwechsel"""
        self.title_label.setText(tr("resin_title"))
        self.lbl_current_resin.setText(tr("resin_current"))
        self.lbl_res_title.setText(tr("resin_summary"))
        self.calculate()

    def calculate(self):
        current_resin = self.spin_resin.value()
        self.progress_bar.setValue(current_resin)
        self.progress_bar.setFormat(tr("resin_progress_format", current=current_resin))

        theme = get_theme()

        if current_resin >= 200:
            self.lbl_time_to_full.setText(tr("resin_full_status"))
            self.lbl_cap_timestamp.setText(tr("resin_cap_time_full"))
            self.lbl_warning_time.setText(tr("resin_warning_full"))
            return

        needed_resin = 200 - current_resin
        seconds_needed = needed_resin * 8 * 60  # 8 minutes per 1 resin

        now = datetime.datetime.now()
        full_time = now + datetime.timedelta(seconds=seconds_needed)
        warning_time = full_time - datetime.timedelta(minutes=30)

        hours = seconds_needed // 3600
        minutes = (seconds_needed % 3600) // 60

        self.lbl_time_to_full.setText(
            tr("resin_time_to_full", color=theme["cyan"], hours=hours, minutes=minutes)
        )
        self.lbl_cap_timestamp.setText(
            tr("resin_cap_timestamp", time_str=full_time.strftime('%H:%M:%S (%A)'))
        )
        self.lbl_warning_time.setText(
            tr("resin_warning_time", color=theme["amber"], time_str=warning_time.strftime('%H:%M:%S'))
        )

    def apply_theme_style(self):
        theme = get_theme()
        self.setStyleSheet(f"""
            ResinPlannerWidget {{
                background-color: {theme['card_bg']};
                border: 1px solid #333847;
                border-radius: 12px;
            }}
            QFrame#sub_card {{
                background-color: #1a1c24;
                border: 1px solid #2d313e;
                border-radius: 8px;
            }}
            QLabel {{
                color: #ffffff;
                font-family: 'Segoe UI', sans-serif;
                font-size: 12px;
            }}
            QSpinBox {{
                background-color: #2a2e3a;
                color: white;
                border: 1px solid {theme['cyan']};
                border-radius: 4px;
                padding: 4px;
                font-size: 11px;
                font-weight: bold;
            }}
            QProgressBar {{
                background-color: #1a1c24;
                color: white;
                border: 1px solid #3d4254;
                border-radius: 6px;
                text-align: center;
                font-weight: bold;
            }}
            QProgressBar::chunk {{
                background-color: {theme['cyan']};
                border-radius: 5px;
            }}
        """)
