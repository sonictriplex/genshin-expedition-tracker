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
from translations import get_translated_book_title, tr


class TeamGoalsWidget(QFrame):
    # Neutrale Mapping-Schlüssel für Charakter -> (Talentbuch-Key, Tage-Key)
    CHARACTER_BOOKS = {
        # Mondstadt
        "Amber": ("book_freedom", "days_mon_thu_sun"),
        "Barbara": ("book_freedom", "days_mon_thu_sun"),
        "Bennett": ("book_resistance", "days_tue_fri_sun"),
        "Diluc": ("book_resistance", "days_tue_fri_sun"),
        "Diona": ("book_freedom", "days_mon_thu_sun"),
        "Eula": ("book_resistance", "days_tue_fri_sun"),
        "Fischl": ("book_resistance", "days_tue_fri_sun"),
        "Jean": ("book_resistance", "days_tue_fri_sun"),
        "Kaeya": ("book_ballad", "days_wed_sat_sun"),
        "Klee": ("book_freedom", "days_mon_thu_sun"),
        "Lisa": ("book_ballad", "days_wed_sat_sun"),
        "Mona": ("book_resistance", "days_tue_fri_sun"),
        "Mika": ("book_ballad", "days_wed_sat_sun"),
        "Noelle": ("book_resistance", "days_tue_fri_sun"),
        "Razor": ("book_resistance", "days_tue_fri_sun"),
        "Rosaria": ("book_ballad", "days_wed_sat_sun"),
        "Sucrose": ("book_freedom", "days_mon_thu_sun"),
        "Traveler (Anemo)": ("book_freedom", "days_mon_thu_sun"),
        "Traveler (Geo)": ("book_prosperity", "days_mon_thu_sun"),
        "Venti": ("book_ballad", "days_wed_sat_sun"),
        # Liyue
        "Beidou": ("book_gold", "days_wed_sat_sun"),
        "Chongyun": ("book_diligence", "days_tue_fri_sun"),
        "Ganyu": ("book_diligence", "days_tue_fri_sun"),
        "Gaming": ("book_prosperity", "days_mon_thu_sun"),
        "Hu Tao": ("book_diligence", "days_tue_fri_sun"),
        "Keqing": ("book_prosperity", "days_mon_thu_sun"),
        "Ningguang": ("book_prosperity", "days_mon_thu_sun"),
        "Qiqi": ("book_prosperity", "days_mon_thu_sun"),
        "Shenhe": ("book_prosperity", "days_mon_thu_sun"),
        "Xiangling": ("book_gold", "days_wed_sat_sun"),
        "Xianyun": ("book_gold", "days_wed_sat_sun"),
        "Xingqiu": ("book_gold", "days_wed_sat_sun"),
        "Xinyan": ("book_gold", "days_wed_sat_sun"),
        "Yanfei": ("book_gold", "days_wed_sat_sun"),
        "Yelan": ("book_prosperity", "days_mon_thu_sun"),
        "Yao Yao": ("book_diligence", "days_tue_fri_sun"),
        "Yun Jin": ("book_diligence", "days_tue_fri_sun"),
        "Zhongli": ("book_gold", "days_wed_sat_sun"),
        # Inazuma
        "Arataki Itto": ("book_elegance", "days_tue_fri_sun"),
        "Gorou": ("book_light", "days_wed_sat_sun"),
        "Kaedehara Kazuha": ("book_diligence", "days_tue_fri_sun"),
        "Kamisato Ayaka": ("book_elegance", "days_tue_fri_sun"),
        "Kamisato Ayato": ("book_elegance", "days_tue_fri_sun"),
        "Kirara": ("book_transience", "days_mon_thu_sun"),
        "Kujou Sara": ("book_elegance", "days_tue_fri_sun"),
        "Kuki Shinobu": ("book_elegance", "days_tue_fri_sun"),
        "Raiden Shogun": ("book_light", "days_wed_sat_sun"),
        "Sangonomiya Kokomi": ("book_transience", "days_mon_thu_sun"),
        "Sayu": ("book_light", "days_wed_sat_sun"),
        "Shikanoin Heizou": ("book_transience", "days_mon_thu_sun"),
        "Thoma": ("book_transience", "days_mon_thu_sun"),
        "Yae Miko": ("book_light", "days_wed_sat_sun"),
        "Yoimiya": ("book_transience", "days_mon_thu_sun"),
        # Sumeru
        "Alhaitham": ("book_ingenuity", "days_tue_fri_sun"),
        "Candace": ("book_admonition", "days_mon_thu_sun"),
        "Collei": ("book_praxis", "days_wed_sat_sun"),
        "Cyno": ("book_admonition", "days_mon_thu_sun"),
        "Dehya": ("book_praxis", "days_wed_sat_sun"),
        "Faruzan": ("book_admonition", "days_mon_thu_sun"),
        "Kaveh": ("book_ingenuity", "days_tue_fri_sun"),
        "Layla": ("book_ingenuity", "days_tue_fri_sun"),
        "Nahida": ("book_ingenuity", "days_tue_fri_sun"),
        "Nilou": ("book_praxis", "days_wed_sat_sun"),
        "Tighnari": ("book_admonition", "days_mon_thu_sun"),
        "Wanderer": ("book_praxis", "days_wed_sat_sun"),
        # Fontaine
        "Arlecchino": ("book_order", "days_wed_sat_sun"),
        "Clorinde": ("book_justice", "days_tue_fri_sun"),
        "Charlotte": ("book_justice", "days_tue_fri_sun"),
        "Chevreuse": ("book_order", "days_wed_sat_sun"),
        "Freminet": ("book_justice", "days_tue_fri_sun"),
        "Furina": ("book_justice", "days_tue_fri_sun"),
        "Lynette": ("book_freedom", "days_mon_thu_sun"),
        "Lyney": ("book_equity", "days_mon_thu_sun"),
        "Navia": ("book_equity", "days_mon_thu_sun"),
        "Neuvillette": ("book_equity", "days_mon_thu_sun"),
        "Wriothesley": ("book_justice", "days_tue_fri_sun"),
        # Natlan
        "Kachina": ("book_conflict", "days_wed_sat_sun"),
        "Kinich": ("book_kindling", "days_tue_fri_sun"),
        "Mualani": ("book_contention", "days_mon_thu_sun"),
        "Xilonen": ("book_kindling", "days_tue_fri_sun"),
    }

    BOOK_KEYS = [
        ("book_freedom", "days_mon_thu_sun"),
        ("book_resistance", "days_tue_fri_sun"),
        ("book_ballad", "days_wed_sat_sun"),
        ("book_prosperity", "days_mon_thu_sun"),
        ("book_diligence", "days_tue_fri_sun"),
        ("book_gold", "days_wed_sat_sun"),
        ("book_transience", "days_mon_thu_sun"),
        ("book_elegance", "days_tue_fri_sun"),
        ("book_light", "days_wed_sat_sun"),
        ("book_admonition", "days_mon_thu_sun"),
        ("book_ingenuity", "days_tue_fri_sun"),
        ("book_praxis", "days_wed_sat_sun"),
        ("book_equity", "days_mon_thu_sun"),
        ("book_justice", "days_tue_fri_sun"),
        ("book_order", "days_wed_sat_sun"),
        ("book_contention", "days_mon_thu_sun"),
        ("book_kindling", "days_tue_fri_sun"),
        ("book_conflict", "days_wed_sat_sun"),
    ]

    def __init__(self, parent_window=None):
        super().__init__(parent_window)
        self.parent_window = parent_window

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(14)
        main_layout.setContentsMargins(16, 16, 16, 16)

        self.title_label = QLabel()
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        main_layout.addWidget(self.title_label)

        grid = QGridLayout()
        grid.setSpacing(12)

        self.lbl_slot_header = QLabel()
        self.lbl_slot_header.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        self.lbl_mat_header = QLabel()
        self.lbl_mat_header.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")

        grid.addWidget(self.lbl_slot_header, 0, 0)
        grid.addWidget(self.lbl_mat_header, 0, 1)

        self.team_inputs = []
        default_team = [
            ("Kaeya", ("book_ballad", "days_wed_sat_sun")),
            ("Fischl", ("book_resistance", "days_tue_fri_sun")),
            ("Xiangling", ("book_gold", "days_wed_sat_sun")),
            ("Barbara", ("book_freedom", "days_mon_thu_sun")),
        ]

        char_list = sorted(list(self.CHARACTER_BOOKS.keys()))

        for i in range(4):
            combo_char = QComboBox()
            combo_char.addItems(char_list)

            combo_book = QComboBox()
            for b_key, d_key in self.BOOK_KEYS:
                combo_book.addItem(get_translated_book_title(b_key, d_key), (b_key, d_key))

            def_char, (def_b_key, def_d_key) = default_team[i]
            idx_char = combo_char.findText(def_char)
            if idx_char >= 0:
                combo_char.setCurrentIndex(idx_char)

            idx_book = self._find_book_index(combo_book, def_b_key, def_d_key)
            if idx_book >= 0:
                combo_book.setCurrentIndex(idx_book)

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

        self.lbl_sum_title = QLabel()
        self.lbl_sum_title.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        v_sum.addWidget(self.lbl_sum_title)

        self.lbl_mon_thu = QLabel()
        self.lbl_tue_fri = QLabel()
        self.lbl_wed_sat = QLabel()
        self.lbl_sun = QLabel()

        v_sum.addWidget(self.lbl_mon_thu)
        v_sum.addWidget(self.lbl_tue_fri)
        v_sum.addWidget(self.lbl_wed_sat)
        v_sum.addWidget(self.lbl_sun)

        main_layout.addWidget(self.summary_card)
        main_layout.addStretch()

        self.retranslate_ui()
        self.apply_theme_style()
        self.update_summary()

    def _find_book_index(self, combo_book, b_key, d_key):
        for idx in range(combo_book.count()):
            data = combo_book.itemData(idx)
            if data == (b_key, d_key):
                return idx
        return -1

    def retranslate_ui(self):
        """Aktualisiert alle UI-Texte dynamisch bei Sprachwechsel"""
        self.title_label.setText(tr("team_title"))
        self.lbl_slot_header.setText(tr("team_char_header"))
        self.lbl_mat_header.setText(tr("team_mat_header"))
        self.lbl_sum_title.setText(tr("team_sum_title"))
        self.lbl_sun.setText(tr("team_sun"))

        # Aktualisiert die Dropdown-Texte der Talentbücher dynamisch
        for _, combo_book in self.team_inputs:
            current_data = combo_book.currentData()  # Aktuelle Auswahl (b_key, d_key) merken
            combo_book.blockSignals(True)
            combo_book.clear()
            
            # Neu befüllen mit der aktuellen Sprache
            for b_key, d_key in self.BOOK_KEYS:
                combo_book.addItem(get_translated_book_title(b_key, d_key), (b_key, d_key))
            
            # Vorherige Auswahl wiederherstellen
            if current_data:
                b_key, d_key = current_data
                idx = self._find_book_index(combo_book, b_key, d_key)
                if idx >= 0:
                    combo_book.setCurrentIndex(idx)
                    
            combo_book.blockSignals(False)

        self.update_summary()

    def on_char_changed(self, char_name, combo_book):
        if char_name in self.CHARACTER_BOOKS:
            b_key, d_key = self.CHARACTER_BOOKS[char_name]
            idx = self._find_book_index(combo_book, b_key, d_key)
            if idx >= 0:
                combo_book.setCurrentIndex(idx)
        self.on_changed()

    def on_changed(self):
        self.update_summary()
        if self.parent_window and hasattr(self.parent_window, "save_expeditions"):
            self.parent_window.save_expeditions()

    def update_summary(self):
        schedule = {
            "days_mon_thu_sun": [],
            "days_tue_fri_sun": [],
            "days_wed_sat_sun": []
        }

        for combo_char, combo_book in self.team_inputs:
            name = combo_char.currentText().strip()
            if not name:
                continue
            data = combo_book.currentData()
            if not data:
                continue
            b_key, d_key = data
            book_name = tr(b_key)

            if d_key in schedule:
                schedule[d_key].append(f"<b>{name}</b> ({book_name})")

        none_str = tr("team_none")
        mon_txt = ", ".join(schedule["days_mon_thu_sun"]) if schedule["days_mon_thu_sun"] else none_str
        tue_txt = ", ".join(schedule["days_tue_fri_sun"]) if schedule["days_tue_fri_sun"] else none_str
        wed_txt = ", ".join(schedule["days_wed_sat_sun"]) if schedule["days_wed_sat_sun"] else none_str

        self.lbl_mon_thu.setText(tr("team_mon_thu", txt=mon_txt))
        self.lbl_tue_fri.setText(tr("team_tue_fri", txt=tue_txt))
        self.lbl_wed_sat.setText(tr("team_wed_sat", txt=wed_txt))

    def get_state_dict(self):
        state = []
        for combo_char, combo_book in self.team_inputs:
            data = combo_book.currentData()
            b_key, d_key = data if data else ("book_freedom", "days_mon_thu_sun")
            state.append({
                "character": combo_char.currentText(),
                "book_key": b_key,
                "days_key": d_key
            })
        return state

    def load_state_dict(self, data):
        if not data or not isinstance(data, list):
            return
        for i, item in enumerate(data):
            if i < len(self.team_inputs):
                combo_char, combo_book = self.team_inputs[i]

                idx_c = combo_char.findText(item.get("character", ""))
                if idx_c >= 0:
                    combo_char.setCurrentIndex(idx_c)

                b_key = item.get("book_key")
                d_key = item.get("days_key")
                if b_key and d_key:
                    idx_b = self._find_book_index(combo_book, b_key, d_key)
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