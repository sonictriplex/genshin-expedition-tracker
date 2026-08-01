from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)
from config import get_theme


class WeeklyBossTrackerWidget(QFrame):
    def __init__(self, parent_window=None):
        super().__init__(parent_window)
        self.parent_window = parent_window

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(14)
        main_layout.setContentsMargins(16, 16, 16, 16)

        title_label = QLabel("🐲 Weekly Boss Discount Tracker (Half Resin)")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        main_layout.addWidget(title_label)

        slots_card = QFrame()
        slots_card.setObjectName("sub_card")
        v_slots = QVBoxLayout(slots_card)
        v_slots.setContentsMargins(12, 12, 12, 12)
        v_slots.setSpacing(8)

        lbl_slots_title = QLabel("WEEKLY 50% RESIN DISCOUNTS (3/3 AVAILABLE)")
        lbl_slots_title.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        v_slots.addWidget(lbl_slots_title)

        h_cb_layout = QHBoxLayout()
        self.cb_discount1 = QCheckBox("Discount Slot 1 (30 Resin)")
        self.cb_discount2 = QCheckBox("Discount Slot 2 (30 Resin)")
        self.cb_discount3 = QCheckBox("Discount Slot 3 (30 Resin)")

        for cb in [self.cb_discount1, self.cb_discount2, self.cb_discount3]:
            cb.stateChanged.connect(self.on_changed)
            h_cb_layout.addWidget(cb)

        v_slots.addLayout(h_cb_layout)
        main_layout.addWidget(slots_card)

        lbl_bosses_header = QLabel("DEFEATED WEEKLY BOSSES THIS WEEK:")
        lbl_bosses_header.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        main_layout.addWidget(lbl_bosses_header)

        grid_bosses = QGridLayout()
        grid_bosses.setSpacing(10)

        boss_list = [
            ("Stormterror Dvalin", "Mondstadt"),
            ("Wolf of the North (Andrius)", "Mondstadt"),
            ("Childe (Enter the Golden House)", "Liyue"),
            ("Azhdaha (Beneath the Dragon-Queller)", "Liyue"),
            ("La Signora (Tenshukaku)", "Inazuma"),
            ("Magatsu Mitake Narukami no Mikoto", "Inazuma"),
            ("Journeyman / Scaramouche", "Sumeru"),
            ("Guardian of Apep's Oasis", "Sumeru"),
            ("All-Devouring Narwhal", "Fontaine"),
            ("Arlecchino (The Knave)", "Fontaine"),
        ]

        self.boss_checkboxes = []
        for i, (boss_name, region) in enumerate(boss_list):
            cb = QCheckBox(f"{boss_name} ({region})")
            cb.stateChanged.connect(self.on_changed)
            row = i // 2
            col = i % 2
            grid_bosses.addWidget(cb, row, col)
            self.boss_checkboxes.append(cb)

        main_layout.addLayout(grid_bosses)

        self.summary_card = QFrame()
        self.summary_card.setObjectName("sub_card")
        v_sum = QVBoxLayout(self.summary_card)
        v_sum.setContentsMargins(12, 12, 12, 12)
        v_sum.setSpacing(8)

        self.lbl_discount_rem = QLabel("Remaining Half-Resin Uses: 3 / 3")
        self.lbl_resin_saved = QLabel("Resin Saved This Week: 0 Resin")

        v_sum.addWidget(self.lbl_discount_rem)
        v_sum.addWidget(self.lbl_resin_saved)

        main_layout.addWidget(self.summary_card)
        main_layout.addStretch()

        self.apply_theme_style()
        self.update_summary()

    def on_changed(self):
        self.update_summary()
        if self.parent_window and hasattr(self.parent_window, "save_expeditions"):
            self.parent_window.save_expeditions()

    def update_summary(self):
        used_discounts = sum([
            1 for cb in [self.cb_discount1, self.cb_discount2, self.cb_discount3] if cb.isChecked()
        ])
        remaining_discounts = 3 - used_discounts
        saved_resin = used_discounts * 30

        theme = get_theme()

        self.lbl_discount_rem.setText(
            f"⚡ Remaining Half-Resin Discounts: <b style='color: {theme['cyan']};'>{remaining_discounts} / 3</b>"
        )
        self.lbl_resin_saved.setText(
            f"💰 Resin Saved This Week: <b style='color: {theme['amber']};'>{saved_resin} Resin</b> "
            f"<span style='color: #aaa;'>(Equivalates to {used_discounts * 4} hours regen time)</span>"
        )

    def get_state_dict(self):
        return {
            "discounts": [
                self.cb_discount1.isChecked(),
                self.cb_discount2.isChecked(),
                self.cb_discount3.isChecked(),
            ],
            "bosses": [cb.isChecked() for cb in self.boss_checkboxes],
        }

    def load_state_dict(self, data):
        if not data:
            return
        discounts = data.get("discounts", [False, False, False])
        if len(discounts) == 3:
            self.cb_discount1.setChecked(discounts[0])
            self.cb_discount2.setChecked(discounts[1])
            self.cb_discount3.setChecked(discounts[2])

        bosses = data.get("bosses", [])
        for i, checked in enumerate(bosses):
            if i < len(self.boss_checkboxes):
                self.boss_checkboxes[i].setChecked(checked)

        self.update_summary()

    def apply_theme_style(self):
        theme = get_theme()
        self.setStyleSheet(f"""
            WeeklyBossTrackerWidget {{
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
            QCheckBox {{
                color: #e6e6e6;
                font-size: 11px;
                font-weight: bold;
            }}
        """)
