from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
)
from config import get_theme


class TeamGoalsWidget(QFrame):
    def __init__(self, parent_window=None):
        super().__init__(parent_window)
        self.parent_window = parent_window

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(14)
        main_layout.setContentsMargins(16, 16, 16, 16)

        # --- Header ---
        title_label = QLabel("🎯 Team Building & Material Farming Goals")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        main_layout.addWidget(title_label)

        # --- Grid Layout for 4 Team Slots ---
        grid = QGridLayout()
        grid.setSpacing(12)

        lbl_slot_header = QLabel("TEAM CHARACTER")
        lbl_slot_header.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        lbl_mat_header = QLabel("TALENT BOOK GOAL")
        lbl_mat_header.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")

        grid.addWidget(lbl_slot_header, 0, 0)
        grid.addWidget(lbl_mat_header, 0, 1)

        self.team_inputs = []
        default_team = [
            ("Kaeya", "Ballad (Wed/Sat)"),
            ("Fischl", "Resistance (Tue/Fri)"),
            ("Noelle", "Resistance (Tue/Fri)"),
            ("Traveler (Anemo)", "Freedom (Mon/Thu)"),
        ]

        book_options = [
            "Freedom (Mon/Thu/Sun)",
            "Resistance (Tue/Fri/Sun)",
            "Ballad (Wed/Sat/Sun)",
            "Prosperity (Mon/Thu/Sun)",
            "Diligence (Tue/Fri/Sun)",
            "Gold (Wed/Sat/Sun)",
        ]

        for i in range(4):
            char_edit = QLineEdit(default_team[i][0])
            combo_book = QComboBox()
            combo_book.addItems(book_options)

            # Select matching default
            for idx, opt in enumerate(book_options):
                if default_team[i][1].split(" ")[0] in opt:
                    combo_book.setCurrentIndex(idx)
                    break

            char_edit.textChanged.connect(self.update_summary)
            combo_book.currentIndexChanged.connect(self.update_summary)

            grid.addWidget(char_edit, i + 1, 0)
            grid.addWidget(combo_book, i + 1, 1)

            self.team_inputs.append((char_edit, combo_book))

        main_layout.addLayout(grid)

        # --- Summary Section ---
        self.summary_card = QFrame()
        self.summary_card.setObjectName("sub_card")
        v_sum = QVBoxLayout(self.summary_card)
        v_sum.setContentsMargins(12, 12, 12, 12)
        v_sum.setSpacing(8)

        lbl_sum_title = QLabel("WEEKLY DOMAIN FARMING SCHEDULE")
        lbl_sum_title.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        v_sum.addWidget(lbl_sum_title)

        self.lbl_mon_thu = QLabel("📅 Mon / Thu: --")
        self.lbl_tue_fri = QLabel("📅 Tue / Fri: --")
        self.lbl_wed_sat = QLabel("📅 Wed / Sat: --")
        self.lbl_sun = QLabel("📅 Sunday: All Talent Domains Open!")

        v_sum.addWidget(self.lbl_mon_thu)
        v_sum.addWidget(self.lbl_tue_fri)
        v_sum.addWidget(self.lbl_wed_sat)
        v_sum.addWidget(self.lbl_sun)

        main_layout.addWidget(self.summary_card)
        main_layout.addStretch()

        self.apply_theme_style()
        self.update_summary()

    def update_summary(self):
        schedule = {
            "Mon/Thu": [],
            "Tue/Fri": [],
            "Wed/Sat": []
        }

        for char_edit, combo_book in self.team_inputs:
            name = char_edit.text().strip()
            if not name:
                continue
            book = combo_book.currentText()

            if "Mon/Thu" in book:
                schedule["Mon/Thu"].append(f"<b>{name}</b> ({book.split(' ')[0]})")
            elif "Tue/Fri" in book:
                schedule["Tue/Fri"].append(f"<b>{name}</b> ({book.split(' ')[0]})")
            elif "Wed/Sat" in book:
                schedule["Wed/Sat"].append(f"<b>{name}</b> ({book.split(' ')[0]})")

        theme = get_theme()

        mon_txt = ", ".join(schedule["Mon/Thu"]) if schedule["Mon/Thu"] else "None"
        tue_txt = ", ".join(schedule["Tue/Fri"]) if schedule["Tue/Fri"] else "None"
        wed_txt = ", ".join(schedule["Wed/Sat"]) if schedule["Wed/Sat"] else "None"

        self.lbl_mon_thu.setText(f"📅 <b>Mon / Thu:</b> {mon_txt}")
        self.lbl_tue_fri.setText(f"📅 <b>Tue / Fri:</b> {tue_txt}")
        self.lbl_wed_sat.setText(f"📅 <b>Wed / Sat:</b> {wed_txt}")

    def apply_theme_style(self):
        theme = get_theme()
        self.setStyleSheet(f"""
            TeamGoalsWidget {{
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
            QLineEdit, QComboBox {{
                background-color: #2a2e3a;
                color: white;
                border: 1px solid {theme['cyan']};
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 11px;
                font-weight: bold;
            }}
        """)
