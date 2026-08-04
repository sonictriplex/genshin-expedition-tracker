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
from translations import tr


class CraftingCalculatorWidget(QFrame):
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

        # --- Grid Layout for Controls ---
        grid = QGridLayout()
        grid.setSpacing(12)

        # 1. Passive Character Selection
        self.lbl_passive = QLabel()
        self.lbl_passive.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        grid.addWidget(self.lbl_passive, 0, 0)

        self.combo_passive = QComboBox()
        self.combo_passive.currentIndexChanged.connect(self.calculate)
        grid.addWidget(self.combo_passive, 0, 1)

        # 2. Inventory Items Input
        self.lbl_inventory = QLabel()
        self.lbl_inventory.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        grid.addWidget(self.lbl_inventory, 1, 0, 1, 2)

        # Tier 1 (Green / 2-Star)
        self.lbl_t1 = QLabel()
        self.spin_t1 = QSpinBox()
        self.spin_t1.setRange(0, 9999)
        self.spin_t1.valueChanged.connect(self.calculate)
        grid.addWidget(self.lbl_t1, 2, 0)
        grid.addWidget(self.spin_t1, 2, 1)

        # Tier 2 (Blue / 3-Star)
        self.lbl_t2 = QLabel()
        self.spin_t2 = QSpinBox()
        self.spin_t2.setRange(0, 9999)
        self.spin_t2.valueChanged.connect(self.calculate)
        grid.addWidget(self.lbl_t2, 3, 0)
        grid.addWidget(self.spin_t2, 3, 1)

        # Tier 3 (Purple / 4-Star)
        self.lbl_t3 = QLabel()
        self.spin_t3 = QSpinBox()
        self.spin_t3.setRange(0, 9999)
        self.spin_t3.valueChanged.connect(self.calculate)
        grid.addWidget(self.lbl_t3, 4, 0)
        grid.addWidget(self.spin_t3, 4, 1)

        main_layout.addLayout(grid)

        # --- Results Box ---
        self.results_card = QFrame()
        self.results_card.setObjectName("sub_card")
        v_res = QVBoxLayout(self.results_card)
        v_res.setContentsMargins(12, 12, 12, 12)
        v_res.setSpacing(8)

        self.lbl_res_title = QLabel()
        self.lbl_res_title.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        v_res.addWidget(self.lbl_res_title)

        self.lbl_out_t2 = QLabel()
        self.lbl_out_t3 = QLabel()
        self.lbl_mora_cost = QLabel()

        v_res.addWidget(self.lbl_out_t2)
        v_res.addWidget(self.lbl_out_t3)
        v_res.addWidget(self.lbl_mora_cost)

        main_layout.addWidget(self.results_card)
        main_layout.addStretch()

        self.retranslate_ui()
        self.apply_theme_style()
        self.calculate()

    def retranslate_ui(self):
        """Aktualisiert alle UI-Texte dynamisch bei Sprachwechsel"""
        self.title_label.setText(tr("craft_title"))
        self.lbl_passive.setText(tr("craft_passive"))
        self.lbl_inventory.setText(tr("craft_inventory"))

        self.lbl_t1.setText(tr("craft_t1"))
        self.lbl_t2.setText(tr("craft_t2"))
        self.lbl_t3.setText(tr("craft_t3"))

        self.lbl_res_title.setText(tr("craft_summary"))

        # Combobox Einträge beibehalten und neu beschriften
        current_data = self.combo_passive.currentData()
        self.combo_passive.blockSignals(True)
        self.combo_passive.clear()
        self.combo_passive.addItem(tr("craft_passive_none"), userData="none")
        self.combo_passive.addItem(tr("craft_passive_double"), userData="double")
        self.combo_passive.addItem(tr("craft_passive_refund"), userData="refund")

        index = self.combo_passive.findData(current_data)
        if index != -1:
            self.combo_passive.setCurrentIndex(index)
        self.combo_passive.blockSignals(False)

        self.calculate()

    def calculate(self):
        t1 = self.spin_t1.value()
        t2 = self.spin_t2.value()
        t3 = self.spin_t3.value()

        passive_mode = self.combo_passive.currentData()

        multiplier = 1.0
        if passive_mode == "double":
            multiplier = 1.10
        elif passive_mode == "refund":
            multiplier = 1.0833

        crafted_t2_from_t1 = math.floor((t1 / 3) * multiplier)
        total_t2 = t2 + crafted_t2_from_t1

        crafted_t3_from_t2 = math.floor((total_t2 / 3) * multiplier)
        total_t3 = t3 + crafted_t3_from_t2

        total_synth_steps = math.floor(t1 / 3) + math.floor(total_t2 / 3)
        estimated_mora = total_synth_steps * 175

        theme = get_theme()
        self.lbl_out_t2.setText(
            tr("craft_out_t2", total=total_t2, crafted=crafted_t2_from_t1)
        )
        self.lbl_out_t3.setText(
            tr("craft_out_t3", total=total_t3, crafted=crafted_t3_from_t2)
        )
        self.lbl_mora_cost.setText(
            tr("craft_mora", color=theme["amber"], mora=estimated_mora)
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
