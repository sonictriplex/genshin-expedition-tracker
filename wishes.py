from datetime import datetime
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QVBoxLayout,
)
from config import get_theme
from translations import tr


class BannerCountdownWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sub_card")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)

        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-size: 11px; font-weight: bold; color: #ffaa00;")

        self.timer_label = QLabel()
        self.timer_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #ffffff;")

        layout.addWidget(self.title_label)
        layout.addWidget(self.timer_label)

        self.banner_end = datetime(2026, 8, 25, 17, 59, 0)

        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_countdown)
        self.clock_timer.start(1000)

        self.retranslate_ui()

    def retranslate_ui(self):
        self.title_label.setText(tr("banner_title"))
        self.update_countdown()

    def update_countdown(self):
        now = datetime.now()
        remaining = self.banner_end - now

        if remaining.total_seconds() <= 0:
            self.timer_label.setText(tr("banner_ended"))
            return

        days = remaining.days
        hours = remaining.seconds // 3600
        minutes = (remaining.seconds % 3600) // 60
        seconds = remaining.seconds % 60

        text = tr("banner_countdown_format", days=days, hours=hours, minutes=minutes, seconds=seconds)
        self.timer_label.setText(text)


class WishPityCounterWidget(QFrame):
    def __init__(self, parent_window=None):
        super().__init__(parent_window)
        self.parent_window = parent_window

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(14)
        main_layout.setContentsMargins(16, 16, 16, 16)

        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        main_layout.addWidget(self.title_label)

        self.banner_countdown = BannerCountdownWidget(self)
        main_layout.addWidget(self.banner_countdown)

        grid = QGridLayout()
        grid.setSpacing(12)

        self.lbl_pity = QLabel()
        self.lbl_pity.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        grid.addWidget(self.lbl_pity, 0, 0)

        self.spin_pity = QSpinBox()
        self.spin_pity.setRange(0, 89)
        self.spin_pity.valueChanged.connect(self.on_changed)
        grid.addWidget(self.spin_pity, 0, 1)

        self.lbl_guaranteed = QLabel()
        self.lbl_guaranteed.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        grid.addWidget(self.lbl_guaranteed, 1, 0)

        self.chk_guaranteed = QCheckBox()
        self.chk_guaranteed.stateChanged.connect(self.on_changed)
        grid.addWidget(self.chk_guaranteed, 1, 1)

        self.lbl_primos = QLabel()
        self.lbl_primos.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        grid.addWidget(self.lbl_primos, 2, 0)

        self.spin_primos = QSpinBox()
        self.spin_primos.setRange(0, 999999)
        self.spin_primos.setSingleStep(160)
        self.spin_primos.valueChanged.connect(self.on_changed)
        grid.addWidget(self.spin_primos, 2, 1)

        self.lbl_fates = QLabel()
        self.lbl_fates.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        grid.addWidget(self.lbl_fates, 3, 0)

        self.spin_fates = QSpinBox()
        self.spin_fates.setRange(0, 9999)
        self.spin_fates.valueChanged.connect(self.on_changed)
        grid.addWidget(self.spin_fates, 3, 1)

        main_layout.addLayout(grid)

        self.results_card = QFrame()
        self.results_card.setObjectName("sub_card")
        v_res = QVBoxLayout(self.results_card)
        v_res.setContentsMargins(12, 12, 12, 12)
        v_res.setSpacing(8)

        self.lbl_res_title = QLabel()
        self.lbl_res_title.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        v_res.addWidget(self.lbl_res_title)

        self.lbl_total_wishes = QLabel()
        self.lbl_to_soft_pity = QLabel()
        self.lbl_to_hard_pity = QLabel()
        self.lbl_guarantee_status = QLabel()

        v_res.addWidget(self.lbl_total_wishes)
        v_res.addWidget(self.lbl_to_soft_pity)
        v_res.addWidget(self.lbl_to_hard_pity)
        v_res.addWidget(self.lbl_guarantee_status)

        main_layout.addWidget(self.results_card)
        main_layout.addStretch()

        self.retranslate_ui()
        self.apply_theme_style()
        self.calculate()

    def retranslate_ui(self):
        """Aktualisiert alle UI-Texte dynamisch bei Sprachwechsel"""
        self.title_label.setText(tr("wish_title"))
        if hasattr(self, "banner_countdown"):
            self.banner_countdown.retranslate_ui()
        self.lbl_pity.setText(tr("wish_current_pity"))
        self.chk_guaranteed.setText(tr("wish_guaranteed"))
        self.lbl_primos.setText(tr("wish_primos"))
        self.lbl_fates.setText(tr("wish_fates"))
        self.lbl_res_title.setText(tr("wish_summary_title"))
        self.calculate()

    def on_changed(self):
        self.calculate()
        if self.parent_window and hasattr(self.parent_window, "save_expeditions"):
            self.parent_window.save_expeditions()

    def calculate(self):
        pity = self.spin_pity.value()
        primos = self.spin_primos.value()
        fates = self.spin_fates.value()
        is_guaranteed = self.chk_guaranteed.isChecked()

        wishes_from_primos = primos // 160
        total_wishes = fates + wishes_from_primos

        wishes_to_soft = max(0, 75 - pity)
        wishes_to_hard = max(0, 90 - pity)

        theme = get_theme()

        self.lbl_total_wishes.setText(tr("wish_total_pulls", color=theme["cyan"], total=total_wishes, primos=wishes_from_primos, fates=fates))
        self.lbl_to_soft_pity.setText(tr("wish_soft_pity", val=wishes_to_soft))
        self.lbl_to_hard_pity.setText(tr("wish_hard_pity", val=wishes_to_hard))

        if is_guaranteed:
            self.lbl_guarantee_status.setText(tr("wish_status_guaranteed"))
        else:
            self.lbl_guarantee_status.setText(tr("wish_status_5050"))

    def get_state_dict(self):
        return {
            "pity": self.spin_pity.value(),
            "guaranteed": self.chk_guaranteed.isChecked(),
            "primogems": self.spin_primos.value(),
            "fates": self.spin_fates.value(),
        }

    def load_state_dict(self, data):
        if not data:
            return
        self.spin_pity.setValue(data.get("pity", 0))
        self.chk_guaranteed.setChecked(data.get("guaranteed", False))
        self.spin_primos.setValue(data.get("primogems", 0))
        self.spin_fates.setValue(data.get("fates", 0))
        self.calculate()

    def apply_theme_style(self):
        theme = get_theme()
        self.setStyleSheet(f"""
            WishPityCounterWidget {{
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
            QCheckBox {{
                color: #e6e6e6;
                font-size: 11px;
                font-weight: bold;
            }}
        """)
        if hasattr(self, "banner_countdown"):
            self.banner_countdown.title_label.setStyleSheet(f"font-size: 11px; font-weight: bold; color: {theme['amber']};")