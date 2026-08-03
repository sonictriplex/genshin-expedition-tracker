from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)
from config import get_theme


class TeamGoalsWidget(QFrame):
    # Mapping von Charakteren zu ihren jeweiligen Talentbüchern
    CHARACTER_BOOKS = {
        # Mondstadt
        "Amber": "Freedom (Mon/Thu/Sun)",
        "Barbara": "Freedom (Mon/Thu/Sun)",
        "Bennett": "Resistance (Tue/Fri/Sun)",
        "Diluc": "Resistance (Tue/Fri/Sun)",
        "Diona": "Freedom (Mon/Thu/Sun)",
        "Eula": "Resistance (Tue/Fri/Sun)",
        "Fischl": "Resistance (Tue/Fri/Sun)",
        "Jean": "Resistance (Tue/Fri/Sun)",
        "Kaeya": "Ballad (Wed/Sat/Sun)",
        "Klee": "Freedom (Mon/Thu/Sun)",
        "Lisa": "Ballad (Wed/Sat/Sun)",
        "Mona": "Resistance (Tue/Fri/Sun)",
        "Mika": "Ballad (Wed/Sat/Sun)",
        "Noelle": "Resistance (Tue/Fri/Sun)",
        "Razor": "Resistance (Tue/Fri/Sun)",
        "Rosaria": "Ballad (Wed/Sat/Sun)",
        "Sucrose": "Freedom (Mon/Thu/Sun)",
        "Traveler (Anemo)": "Freedom (Mon/Thu/Sun)",
        "Traveler (Geo)": "Prosperity (Mon/Thu/Sun)",
        "Venti": "Ballad (Wed/Sat/Sun)",

        # Liyue
        "Beidou": "Gold (Wed/Sat/Sun)",
        "Chongyun": "Diligence (Tue/Fri/Sun)",
        "Ganyu": "Diligence (Tue/Fri/Sun)",
        "Gaming": "Prosperity (Mon/Thu/Sun)",
        "Hu Tao": "Diligence (Tue/Fri/Sun)",
        "Keqing": "Prosperity (Mon/Thu/Sun)",
        "Ningguang": "Prosperity (Mon/Thu/Sun)",
        "Qiqi": "Prosperity (Mon/Thu/Sun)",
        "Shenhe": "Prosperity (Mon/Thu/Sun)",
        "Xiangling": "Gold (Wed/Sat/Sun)",
        "Xianyun": "Gold (Wed/Sat/Sun)",
        "Xingqiu": "Gold (Wed/Sat/Sun)",
        "Xinyan": "Gold (Wed/Sat/Sun)",
        "Yanfei": "Gold (Wed/Sat/Sun)",
        "Yelan": "Prosperity (Mon/Thu/Sun)",
        "Yao Yao": "Diligence (Tue/Fri/Sun)",
        "Yun Jin": "Diligence (Tue/Fri/Sun)",
        "Zhongli": "Gold (Wed/Sat/Sun)",

        # Inazuma
        "Arataki Itto": "Elegance (Tue/Fri/Sun)",
        "Gorou": "Light (Wed/Sat/Sun)",
        "Kaedehara Kazuha": "Diligence (Tue/Fri/Sun)",
        "Kamisato Ayaka": "Elegance (Tue/Fri/Sun)",
        "Kamisato Ayato": "Elegance (Tue/Fri/Sun)",
        "Kirara": "Transience (Mon/Thu/Sun)",
        "Kujou Sara": "Elegance (Tue/Fri/Sun)",
        "Kuki Shinobu": "Elegance (Tue/Fri/Sun)",
        "Raiden Shogun": "Light (Wed/Sat/Sun)",
        "Sangonomiya Kokomi": "Transience (Mon/Thu/Sun)",
        "Sayu": "Light (Wed/Sat/Sun)",
        "Shikanoin Heizou": "Transience (Mon/Thu/Sun)",
        "Thoma": "Transience (Mon/Thu/Sun)",
        "Yae Miko": "Light (Wed/Sat/Sun)",
        "Yoimiya": "Transience (Mon/Thu/Sun)",

        # Sumeru
        "Alhaitham": "Ingenuity (Tue/Fri/Sun)",
        "Candace": "Admonition (Mon/Thu/Sun)",
        "Collei": "Praxis (Wed/Sat/Sun)",
        "Cyno": "Admonition (Mon/Thu/Sun)",
        "Dehya": "Praxis (Wed/Sat/Sun)",
        "Faruzan": "Admonition (Mon/Thu/Sun)",
        "Kaveh": "Ingenuity (Tue/Fri/Sun)",
        "Layla": "Ingenuity (Tue/Fri/Sun)",
        "Nahida": "Ingenuity (Tue/Fri/Sun)",
        "Nilou": "Praxis (Wed/Sat/Sun)",
        "Tighnari": "Admonition (Mon/Thu/Sun)",
        "Wanderer": "Praxis (Wed/Sat/Sun)",

        # Fontaine
        "Arlecchino": "Order (Wed/Sat/Sun)",
        "Clorinde": "Justice (Tue/Fri/Sun)",
        "Charlotte": "Justice (Tue/Fri/Sun)",
        "Chevreuse": "Order (Wed/Sat/Sun)",
        "Freminet": "Justice (Tue/Fri/Sun)",
        "Furina": "Justice (Tue/Fri/Sun)",
        "Lynette": "Freedom (Mon/Thu/Sun)",
        "Lyney": "Equity (Mon/Thu/Sun)",
        "Navia": "Equity (Mon/Thu/Sun)",
        "Neuvillette": "Equity (Mon/Thu/Sun)",
        "Wriothesley": "Justice (Tue/Fri/Sun)",

        # Natlan
        "Kachina": "Conflict (Wed/Sat/Sun)",
        "Kinich": "Kindling (Tue/Fri/Sun)",
        "Mualani": "Contention (Mon/Thu/Sun)",
        "Xilonen": "Kindling (Tue/Fri/Sun)",
    }

    def __init__(self, parent_window=None):
        super().__init__(parent_window)
        self.parent_window = parent_window

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(14)
        main_layout.setContentsMargins(16, 16, 16, 16)

        title_label = QLabel("🎯 Team Building & Material Farming Goals")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        main_layout.addWidget(title_label)

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
            ("Kaeya", "Ballad (Wed/Sat/Sun)"),
            ("Fischl", "Resistance (Tue/Fri/Sun)"),
            ("Xiangling", "Gold (Wed/Sat/Sun)"),
            ("Barbara", "Freedom (Mon/Thu/Sun)"),
        ]

        book_options = [
            # Mondstadt
            "Freedom (Mon/Thu/Sun)",
            "Resistance (Tue/Fri/Sun)",
            "Ballad (Wed/Sat/Sun)",
            # Liyue
            "Prosperity (Mon/Thu/Sun)",
            "Diligence (Tue/Fri/Sun)",
            "Gold (Wed/Sat/Sun)",
            # Inazuma
            "Transience (Mon/Thu/Sun)",
            "Elegance (Tue/Fri/Sun)",
            "Light (Wed/Sat/Sun)",
            # Sumeru
            "Admonition (Mon/Thu/Sun)",
            "Ingenuity (Tue/Fri/Sun)",
            "Praxis (Wed/Sat/Sun)",
            # Fontaine
            "Equity (Mon/Thu/Sun)",
            "Justice (Tue/Fri/Sun)",
            "Order (Wed/Sat/Sun)",
            # Natlan
            "Contention (Mon/Thu/Sun)",
            "Kindling (Tue/Fri/Sun)",
            "Conflict (Wed/Sat/Sun)",
        ]

        char_list = sorted(list(self.CHARACTER_BOOKS.keys()))

        for i in range(4):
            combo_char = QComboBox()
            combo_char.addItems(char_list)

            combo_book = QComboBox()
            combo_book.addItems(book_options)

            # Standardwerte für dein aktuelles Team setzen
            def_char, def_book = default_team[i]
            idx_char = combo_char.findText(def_char)
            if idx_char >= 0:
                combo_char.setCurrentIndex(idx_char)

            idx_book = combo_book.findText(def_book)
            if idx_book >= 0:
                combo_book.setCurrentIndex(idx_book)

            # Signale verbinden
            combo_char.currentTextChanged.connect(
                lambda text, cb=combo_book: self.on_char_changed(text, cb)
            )
            combo_book.currentIndexChanged.connect(self.on_changed)

            grid.addWidget(combo_char, i + 1, 0)
            grid.addWidget(combo_book, i + 1, 1)

            self.team_inputs.append((combo_char, combo_book))

        main_layout.addLayout(grid)

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

    def on_char_changed(self, char_name, combo_book):
        """Passives Talentbuch automatisch wählen, wenn ein Charakter gewählt wird."""
        if char_name in self.CHARACTER_BOOKS:
            target_book = self.CHARACTER_BOOKS[char_name]
            idx = combo_book.findText(target_book)
            if idx >= 0:
                combo_book.setCurrentIndex(idx)
        self.on_changed()

    def on_changed(self):
        self.update_summary()
        if self.parent_window and hasattr(self.parent_window, "save_expeditions"):
            self.parent_window.save_expeditions()

    def update_summary(self):
        schedule = {
            "Mon/Thu": [],
            "Tue/Fri": [],
            "Wed/Sat": []
        }

        for combo_char, combo_book in self.team_inputs:
            name = combo_char.currentText().strip()
            if not name:
                continue
            book = combo_book.currentText()
            book_name = book.split(' ')[0]

            if "Mon/Thu" in book:
                schedule["Mon/Thu"].append(f"<b>{name}</b> ({book_name})")
            elif "Tue/Fri" in book:
                schedule["Tue/Fri"].append(f"<b>{name}</b> ({book_name})")
            elif "Wed/Sat" in book:
                schedule["Wed/Sat"].append(f"<b>{name}</b> ({book_name})")

        mon_txt = ", ".join(schedule["Mon/Thu"]) if schedule["Mon/Thu"] else "None"
        tue_txt = ", ".join(schedule["Tue/Fri"]) if schedule["Tue/Fri"] else "None"
        wed_txt = ", ".join(schedule["Wed/Sat"]) if schedule["Wed/Sat"] else "None"

        self.lbl_mon_thu.setText(f"📅 <b>Mon / Thu:</b> {mon_txt}")
        self.lbl_tue_fri.setText(f"📅 <b>Tue / Fri:</b> {tue_txt}")
        self.lbl_wed_sat.setText(f"📅 <b>Wed / Sat:</b> {wed_txt}")

    def get_state_dict(self):
        return [
            {
                "character": combo_char.currentText(),
                "book": combo_book.currentText()
            }
            for combo_char, combo_book in self.team_inputs
        ]

    def load_state_dict(self, data):
        if not data or not isinstance(data, list):
            return
        for i, item in enumerate(data):
            if i < len(self.team_inputs):
                combo_char, combo_book = self.team_inputs[i]

                # Charakter setzen
                idx_c = combo_char.findText(item.get("character", ""))
                if idx_c >= 0:
                    combo_char.setCurrentIndex(idx_c)

                # Buch setzen
                idx_b = combo_book.findText(item.get("book", ""))
                if idx_b >= 0:
                    combo_book.setCurrentIndex(idx_b)

        self.update_summary()

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
            QComboBox {{
                background-color: #2a2e3a;
                color: white;
                border: 1px solid {theme['cyan']};
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 11px;
                font-weight: bold;
            }}
        """)
