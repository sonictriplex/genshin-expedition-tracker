from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

from config import (
    CHARACTERS,
    REGIONS,
    RESOURCES,
    TIME_REDUCTION_BONUS,
    get_theme,
    is_autostart_enabled,
)


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
        theme = get_theme()

        self.setFixedSize(380, 260)
        self.setStyleSheet(f"""
            InlineAddDialog {{
                background-color: {theme['card_bg']};
                border: 2px solid {theme['cyan']};
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
            QComboBox:focus {{ border: 1px solid {theme['cyan']}; }}
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
                background-color: {theme['cyan']};
                color: #1a1c24;
                border: none;
            }}
            QPushButton[primary="true"]:hover {{ background-color: {theme['cyan']}; }}
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)

        lbl_title = QLabel("New Expedition")
        lbl_title.setStyleSheet(f"font-size: 14px; color: {theme['cyan']}; margin-bottom: 5px;")
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


class InlineResinDialog(QFrame):
    def __init__(self, current_resin=120, max_resin=200, on_submit=None, on_cancel=None, parent=None):
        super().__init__(parent)
        self.on_submit_callback = on_submit
        self.on_cancel_callback = on_cancel
        self.max_resin = max_resin
        theme = get_theme()

        self.setFixedSize(320, 180)
        self.setStyleSheet(f"""
            InlineResinDialog {{
                background-color: {theme['card_bg']};
                border: 2px solid {theme['cyan']};
                border-radius: 12px;
            }}
            QLabel {{ color: #e6e6e6; font-weight: bold; font-size: 12px; }}
            QSpinBox {{
                background-color: #1a1c24;
                color: white;
                border: 1px solid #3d4254;
                border-radius: 5px;
                padding: 5px 36px 5px 8px;
                font-size: 14px;
                font-weight: bold;
            }}
            QSpinBox:focus {{ border: 1px solid {theme['cyan']}; }}
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
                background-color: {theme['cyan']};
                color: #1a1c24;
                border: none;
            }}
            QPushButton[primary="true"]:hover {{ background-color: {theme['cyan']}; }}
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)

        lbl_title = QLabel("Adjust Original Resin")
        lbl_title.setStyleSheet(f"font-size: 14px; color: {theme['cyan']}; margin-bottom: 5px;")
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


class InlineSettingsDialog(QFrame):
    def __init__(self, close_to_tray=True, on_submit=None, on_cancel=None, parent=None):
        super().__init__(parent)
        self.on_submit_callback = on_submit
        self.on_cancel_callback = on_cancel
        theme = get_theme()

        self.setFixedSize(380, 220)
        self.setStyleSheet(f"""
            InlineSettingsDialog {{
                background-color: {theme['card_bg']};
                border: 2px solid {theme['cyan']};
                border-radius: 12px;
            }}
            QLabel {{ color: #e6e6e6; font-weight: bold; font-size: 12px; }}
            QCheckBox {{
                color: white;
                font-size: 12px;
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border-radius: 4px;
                border: 1px solid #3d4254;
                background-color: #1a1c24;
            }}
            QCheckBox::indicator:checked {{
                background-color: {theme['cyan']};
                border: 1px solid {theme['cyan']};
            }}
            QComboBox {{
                background-color: #1a1c24;
                color: white;
                border: 1px solid #3d4254;
                border-radius: 5px;
                padding: 4px 8px;
                font-size: 12px;
            }}
            QPushButton {{
                background-color: #2e323f;
                color: white;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 6px 14px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: #3b3f54; }}
            QPushButton[primary="true"] {{
                background-color: {theme['cyan']};
                color: #1a1c24;
                border: none;
            }}
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)

        lbl_title = QLabel("⚙️ Settings")
        lbl_title.setStyleSheet(f"font-size: 14px; color: {theme['cyan']}; margin-bottom: 4px;")
        layout.addWidget(lbl_title)

        # Autostart Option
        self.chk_autostart = QCheckBox("Start with System (Autostart)")
        self.chk_autostart.setChecked(is_autostart_enabled())
        layout.addWidget(self.chk_autostart)

        # Close Action Option
        lbl_close_action = QLabel("On Window Close (✕):")
        layout.addWidget(lbl_close_action)

        self.combo_close_action = QComboBox()
        self.combo_close_action.addItem("Minimize to System Tray", userData=True)
        self.combo_close_action.addItem("Exit Application", userData=False)

        idx = 0 if close_to_tray else 1
        self.combo_close_action.setCurrentIndex(idx)
        layout.addWidget(self.combo_close_action)

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
        autostart = self.chk_autostart.isChecked()
        close_to_tray = self.combo_close_action.currentData()
        if self.on_submit_callback:
            self.on_submit_callback(autostart, close_to_tray)

    def cancel_click(self):
        if self.on_cancel_callback:
            self.on_cancel_callback()
