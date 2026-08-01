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


class ResinPlannerWidget(QFrame):
    def __init__(self, parent_window=None):
        super().__init__(parent_window)
        self.parent_window = parent_window

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(14)
        main_layout.setContentsMargins(16, 16, 16, 16)

        # --- Header ---
        title_label = QLabel("⚡ Original Resin Overflow & Cap Planner")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        main_layout.addWidget(title_label)

        # --- Grid Layout for Input ---
        grid = QGridLayout()
        grid.setSpacing(12)

        lbl_current_resin = QLabel("Current Resin Amount:")
        lbl_current_resin.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        grid.addWidget(lbl_current_resin, 0, 0)

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

        lbl_res_title = QLabel("RESIN REGENERATION SUMMARY")
        lbl_res_title.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        v_res.addWidget(lbl_res_title)

        self.lbl_time_to_full = QLabel("Time until 200/200: --")
        self.lbl_cap_timestamp = QLabel("Exact Full Cap Time: --")
        self.lbl_warning_time = QLabel("Warning Trigger (30m before cap): --")

        v_res.addWidget(self.lbl_time_to_full)
        v_res.addWidget(self.lbl_cap_timestamp)
        v_res.addWidget(self.lbl_warning_time)

        main_layout.addWidget(self.results_card)
        main_layout.addStretch()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.calculate)
        self.timer.start(10000)  # Refresh every 10 seconds

        self.apply_theme_style()
        self.calculate()

    def calculate(self):
        current_resin = self.spin_resin.value()
        self.progress_bar.setValue(current_resin)
        self.progress_bar.setFormat(f"{current_resin} / 200 Resin")

        theme = get_theme()

        if current_resin >= 200:
            self.lbl_time_to_full.setText("⚡ Status: <b style='color: #ff5555;'>RESIN IS FULL (MAX CAP)!</b>")
            self.lbl_cap_timestamp.setText("Exact Full Cap Time: <b>Already Capped</b>")
            self.lbl_warning_time.setText("Warning Trigger: <b>Overlapping Capacity</b>")
            return

        needed_resin = 200 - current_resin
        seconds_needed = needed_resin * 8 * 60  # 8 minutes per 1 resin

        now = datetime.datetime.now()
        full_time = now + datetime.timedelta(seconds=seconds_needed)
        warning_time = full_time - datetime.timedelta(minutes=30)

        hours = seconds_needed // 3600
        minutes = (seconds_needed % 3600) // 60

        self.lbl_time_to_full.setText(
            f"⏳ Time to Full (200/200): <b style='color: {theme['cyan']};'>{hours}h {minutes}m</b>"
        )
        self.lbl_cap_timestamp.setText(
            f"📅 Exact Full Cap Time: <b>{full_time.strftime('%H:%M:%S (%A)')}</b>"
        )
        self.lbl_warning_time.setText(
            f"🔔 Warning Time (30m Before Cap): <b style='color: {theme['amber']};'>{warning_time.strftime('%H:%M:%S')}</b>"
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
