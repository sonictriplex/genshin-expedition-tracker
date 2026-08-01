from PyQt6.QtCore import Qt
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


class WishPityCounterWidget(QFrame):
    def __init__(self, parent_window=None):
        super().__init__(parent_window)
        self.parent_window = parent_window

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(14)
        main_layout.setContentsMargins(16, 16, 16, 16)

        # --- Header ---
        title_label = QLabel("🌠 Wish & Pity Savings Counter")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        main_layout.addWidget(title_label)

        # --- Grid Layout for Controls ---
        grid = QGridLayout()
        grid.setSpacing(12)

        # Current Pity
        lbl_pity = QLabel("Current Pity (Wishes since last 5★):")
        lbl_pity.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        grid.addWidget(lbl_pity, 0, 0)

        self.spin_pity = QSpinBox()
        self.spin_pity.setRange(0, 89)
        self.spin_pity.valueChanged.connect(self.calculate)
        grid.addWidget(self.spin_pity, 0, 1)

        # 50/50 Status
        lbl_guaranteed = QLabel("50/50 Status:")
        lbl_guaranteed.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        grid.addWidget(lbl_guaranteed, 1, 0)

        self.chk_guaranteed = QCheckBox("Next 5★ is Guaranteed (Lost last 50/50)")
        self.chk_guaranteed.stateChanged.connect(self.calculate)
        grid.addWidget(self.chk_guaranteed, 1, 1)

        # Savings Input: Primogems
        lbl_primos = QLabel("💎 Primogems Owned:")
        lbl_primos.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        grid.addWidget(lbl_primos, 2, 0)

        self.spin_primos = QSpinBox()
        self.spin_primos.setRange(0, 999999)
        self.spin_primos.setSingleStep(160)
        self.spin_primos.valueChanged.connect(self.calculate)
        grid.addWidget(self.spin_primos, 2, 1)

        # Savings Input: Intertwined Fates
        lbl_fates = QLabel("💫 Intertwined Fates Owned:")
        lbl_fates.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        grid.addWidget(lbl_fates, 3, 0)

        self.spin_fates = QSpinBox()
        self.spin_fates.setRange(0, 9999)
        self.spin_fates.valueChanged.connect(self.calculate)
        grid.addWidget(self.spin_fates, 3, 1)

        main_layout.addLayout(grid)

        # --- Results Box ---
        self.results_card = QFrame()
        self.results_card.setObjectName("sub_card")
        v_res = QVBoxLayout(self.results_card)
        v_res.setContentsMargins(12, 12, 12, 12)
        v_res.setSpacing(8)

        lbl_res_title = QLabel("PITY & SAVINGS SUMMARY")
        lbl_res_title.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        v_res.addWidget(lbl_res_title)

        self.lbl_total_wishes = QLabel("Total Available Wishes: 0")
        self.lbl_to_soft_pity = QLabel("Wishes to Soft Pity (75): 75")
        self.lbl_to_hard_pity = QLabel("Wishes to Hard Pity (90): 90")
        self.lbl_guarantee_status = QLabel("Target Guarantee: 50/50 Chance")

        v_res.addWidget(self.lbl_total_wishes)
        v_res.addWidget(self.lbl_to_soft_pity)
        v_res.addWidget(self.lbl_to_hard_pity)
        v_res.addWidget(self.lbl_guarantee_status)

        main_layout.addWidget(self.results_card)
        main_layout.addStretch()

        self.apply_theme_style()
        self.calculate()

    def calculate(self):
        pity = self.spin_pity.value()
        primos = self.spin_primos.value()
        fates = self.spin_fates.value()
        is_guaranteed = self.chk_guaranteed.isChecked()

        # Calculation
        wishes_from_primos = primos // 160
        total_wishes = fates + wishes_from_primos
        effective_pity_total = pity + total_wishes

        wishes_to_soft = max(0, 75 - pity)
        wishes_to_hard = max(0, 90 - pity)

        theme = get_theme()

        self.lbl_total_wishes.setText(
            f"💫 Total Available Pulls: <b style='color: {theme['cyan']};'>{total_wishes} Wishes</b> "
            f"<span style='color: #aaa;'>(From {wishes_from_primos} primos + {fates} fates)</span>"
        )
        self.lbl_to_soft_pity.setText(
            f"🎯 Wishes to Soft Pity (75): <b>{wishes_to_soft}</b>"
        )
        self.lbl_to_hard_pity.setText(
            f"🛡️ Wishes to Hard Pity (90): <b>{wishes_to_hard}</b>"
        )

        if is_guaranteed:
            self.lbl_guarantee_status.setText(
                "✨ Target Status: <b style='color: #55ff55;'>GUARANTEED 5★ Character</b>"
            )
        else:
            self.lbl_guarantee_status.setText(
                "🎲 Target Status: <b style='color: #ffaa00;'>50/50 Chance</b>"
            )

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
