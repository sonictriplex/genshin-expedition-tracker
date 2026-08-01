import math
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)
from config import get_theme


class CraftingCalculatorWidget(QFrame):
    def __init__(self, parent_window=None):
        super().__init__(parent_window)
        self.parent_window = parent_window

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(14)
        main_layout.setContentsMargins(16, 16, 16, 16)

        # --- Header ---
        title_label = QLabel("🧪 Alchemy & Crafting Bench Calculator")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        main_layout.addWidget(title_label)

        # --- Grid Layout for Controls ---
        grid = QGridLayout()
        grid.setSpacing(12)

        # 1. Passive Character Selection
        lbl_passive = QLabel("Crafting Passive (Char Bonus):")
        lbl_passive.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        grid.addWidget(lbl_passive, 0, 0)

        self.combo_passive = QComboBox()
        self.combo_passive.addItem("None (Standard 3:1)", userData="none")
        self.combo_passive.addItem("Sucrose / Albedo (10% Chance for 2x Product)", userData="double")
        self.combo_passive.addItem("Mona / Xingqiu (25% Chance to Refund Material)", userData="refund")
        self.combo_passive.currentIndexChanged.connect(self.calculate)
        grid.addWidget(self.combo_passive, 0, 1)

        # 2. Inventory Items Input
        lbl_inventory = QLabel("CURRENT INVENTORY:")
        lbl_inventory.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        grid.addWidget(lbl_inventory, 1, 0, 1, 2)

        # Tier 1 (Green / 2-Star)
        lbl_t1 = QLabel("🟢 Tier 1 (Green / 2★):")
        self.spin_t1 = QSpinBox()
        self.spin_t1.setRange(0, 9999)
        self.spin_t1.valueChanged.connect(self.calculate)
        grid.addWidget(lbl_t1, 2, 0)
        grid.addWidget(self.spin_t1, 2, 1)

        # Tier 2 (Blue / 3-Star)
        lbl_t2 = QLabel("🔵 Tier 2 (Blue / 3★):")
        self.spin_t2 = QSpinBox()
        self.spin_t2.setRange(0, 9999)
        self.spin_t2.valueChanged.connect(self.calculate)
        grid.addWidget(lbl_t2, 3, 0)
        grid.addWidget(self.spin_t2, 3, 1)

        # Tier 3 (Purple / 4-Star)
        lbl_t3 = QLabel("🟣 Tier 3 (Purple / 4★):")
        self.spin_t3 = QSpinBox()
        self.spin_t3.setRange(0, 9999)
        self.spin_t3.valueChanged.connect(self.calculate)
        grid.addWidget(lbl_t3, 4, 0)
        grid.addWidget(self.spin_t3, 4, 1)

        main_layout.addLayout(grid)

        # --- Results Box ---
        self.results_card = QFrame()
        self.results_card.setObjectName("sub_card")
        v_res = QVBoxLayout(self.results_card)
        v_res.setContentsMargins(12, 12, 12, 12)
        v_res.setSpacing(8)

        lbl_res_title = QLabel("CRAFTING SUMMARY & OUTPUT")
        lbl_res_title.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        v_res.addWidget(lbl_res_title)

        self.lbl_out_t2 = QLabel("Max Blue Materials (3★): 0")
        self.lbl_out_t3 = QLabel("Max Purple Materials (4★): 0")
        self.lbl_mora_cost = QLabel("Estimated Mora Cost: 0 Mora")

        v_res.addWidget(self.lbl_out_t2)
        v_res.addWidget(self.lbl_out_t3)
        v_res.addWidget(self.lbl_mora_cost)

        main_layout.addWidget(self.results_card)
        main_layout.addStretch()

        self.apply_theme_style()
        self.calculate()

    def calculate(self):
        t1 = self.spin_t1.value()
        t2 = self.spin_t2.value()
        t3 = self.spin_t3.value()

        passive_mode = self.combo_passive.currentData()

        # Multipliers based on passive character traits
        # 'double' = +10% expected value on crafted items
        # 'refund' = +8.33% effective savings (1/3 material refunded 25% of the time = 1/12 effective refund)
        multiplier = 1.0
        if passive_mode == "double":
            multiplier = 1.10
        elif passive_mode == "refund":
            multiplier = 1.0833

        # Calculations from T1 to T2
        crafted_t2_from_t1 = math.floor((t1 / 3) * multiplier)
        total_t2 = t2 + crafted_t2_from_t1

        # Calculations from T2 to T3
        crafted_t3_from_t2 = math.floor((total_t2 / 3) * multiplier)
        total_t3 = t3 + crafted_t3_from_t2

        # Mora calculation (Standard Genshin crafting costs: 175 Mora per synth step for books/mats)
        total_synth_steps = math.floor(t1 / 3) + math.floor(total_t2 / 3)
        estimated_mora = total_synth_steps * 175

        # Update UI labels
        theme = get_theme()
        self.lbl_out_t2.setText(
            f"🔵 Total Blue Materials (3★): <b>{total_t2}</b> "
            f"<span style='color: #aaa;'>(+ {crafted_t2_from_t1} crafted)</span>"
        )
        self.lbl_out_t3.setText(
            f"🟣 Max Purple Materials (4★): <b>{total_t3}</b> "
            f"<span style='color: #aaa;'>(+ {crafted_t3_from_t2} crafted)</span>"
        )
        self.lbl_mora_cost.setText(
            f"💰 Estimated Crafting Cost: <b style='color: {theme['amber']};'>{estimated_mora:,} Mora</b>"
        )

    def apply_theme_style(self):
        theme = get_theme()
        self.setStyleSheet(f"""
            CraftingCalculatorWidget {{
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
            QComboBox, QSpinBox {{
                background-color: #2a2e3a;
                color: white;
                border: 1px solid {theme['cyan']};
                border-radius: 4px;
                padding: 4px;
                font-size: 11px;
                font-weight: bold;
            }}
        """)
