import time
from datetime import datetime
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)
from config import get_theme


class TeyvatJournalWidget(QFrame):
    def __init__(self, parent_window=None):
        super().__init__(parent_window)
        self.parent_window = parent_window

        # Statustimer
        self.transformer_end_time = 0.0
        self.artifact_end_time = 0.0

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(14, 12, 14, 12)

        # --- Header mit AR-Stufen-Auswahl ---
        header_layout = QHBoxLayout()
        title_label = QLabel("📖 Teyvat Reisetagebuch & Checklisten")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff;")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        lbl_ar = QLabel("Abenteuerstufe (AR):")
        lbl_ar.setStyleSheet("font-size: 11px; font-weight: bold; color: #aaa;")
        header_layout.addWidget(lbl_ar)

        # Standard auf AR 21
        self.spin_ar = QSpinBox()
        self.spin_ar.setRange(1, 60)
        self.spin_ar.setValue(21)
        self.spin_ar.setToolTip("Schaltet Features basierend auf deiner Abenteuerstufe frei.")
        self.spin_ar.valueChanged.connect(self.on_ar_changed)
        header_layout.addWidget(self.spin_ar)

        main_layout.addLayout(header_layout)

        # --- GRID FÜR CARDS ---
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(10)

        # =========================================================================
        # Box 1: Daily Commissions & Katheryne (Ab AR 1)
        # =========================================================================
        self.box_comm = QFrame()
        self.box_comm.setObjectName("sub_card")
        v_comm = QVBoxLayout(self.box_comm)
        v_comm.setContentsMargins(10, 8, 10, 8)
        v_comm.setSpacing(6)

        lbl_comm = QLabel("TÄGLICHE MISSIONEN")
        lbl_comm.setStyleSheet("font-size: 10px; font-weight: bold; color: #aaa;")
        v_comm.addWidget(lbl_comm)

        h_comm = QHBoxLayout()
        self.comm_boxes = []
        for i in range(4):
            cb = QCheckBox(f"#{i+1}")
            cb.stateChanged.connect(self.on_state_changed)
            h_comm.addWidget(cb)
            self.comm_boxes.append(cb)

        self.katheryne_cb = QCheckBox("🎁 Katheryne")
        self.katheryne_cb.stateChanged.connect(self.on_state_changed)
        h_comm.addWidget(self.katheryne_cb)
        h_comm.addStretch()
        v_comm.addLayout(h_comm)

        self.grid_layout.addWidget(self.box_comm, 0, 0)

        # =========================================================================
        # Box 2: Wochenbosse & Material-Rotation (Ab AR 1)
        # =========================================================================
        self.box_boss = QFrame()
        self.box_boss.setObjectName("sub_card")
        v_boss = QVBoxLayout(self.box_boss)
        v_boss.setContentsMargins(10, 8, 10, 8)
        v_boss.setSpacing(6)

        lbl_boss = QLabel("WOCHENBOSSE & ROTATION")
        lbl_boss.setStyleSheet("font-size: 10px; font-weight: bold; color: #aaa;")
        v_boss.addWidget(lbl_boss)

        h_boss = QHBoxLayout()
        self.boss_boxes = []
        for i in range(3):
            cb = QCheckBox(f"Boss #{i+1}")
            cb.stateChanged.connect(self.on_state_changed)
            h_boss.addWidget(cb)
            self.boss_boxes.append(cb)
        h_boss.addStretch()
        v_boss.addLayout(h_boss)

        self.rotation_label = QLabel(self.get_today_rotation())
        self.rotation_label.setWordWrap(True)
        v_boss.addWidget(self.rotation_label)

        self.grid_layout.addWidget(self.box_boss, 0, 1)

        # =========================================================================
        # Box 3: Kannenreich-Manager (Freigeschaltet ab AR 28)
        # =========================================================================
        self.box_pot = QFrame()
        self.box_pot.setObjectName("sub_card")
        v_pot = QVBoxLayout(self.box_pot)
        v_pot.setContentsMargins(10, 8, 10, 8)
        v_pot.setSpacing(6)

        lbl_pot = QLabel("KANNENREICH (AB AR 28)")
        lbl_pot.setStyleSheet("font-size: 10px; font-weight: bold; color: #aaa;")
        v_pot.addWidget(lbl_pot)

        h_pot_items = QHBoxLayout()
        self.pot_resin_cb = QCheckBox("Flüchtiges Harz")
        self.pot_resin_cb.stateChanged.connect(self.on_state_changed)
        self.pot_books_cb = QCheckBox("XP/Bücher")
        self.pot_books_cb.stateChanged.connect(self.on_state_changed)
        self.pot_arte_cb = QCheckBox("Artefakt-Münzen")
        self.pot_arte_cb.stateChanged.connect(self.on_state_changed)

        h_pot_items.addWidget(self.pot_resin_cb)
        h_pot_items.addWidget(self.pot_books_cb)
        h_pot_items.addWidget(self.pot_arte_cb)
        h_pot_items.addStretch()
        v_pot.addLayout(h_pot_items)

        self.grid_layout.addWidget(self.box_pot, 1, 0)

        # =========================================================================
        # Box 4: Parametrischer Konverter (Freigeschaltet ab AR 31)
        # =========================================================================
        self.box_trans = QFrame()
        self.box_trans.setObjectName("sub_card")
        v_trans = QVBoxLayout(self.box_trans)
        v_trans.setContentsMargins(10, 8, 10, 8)
        v_trans.setSpacing(6)

        lbl_trans = QLabel("PARAMETRISCHER KONVERTER (AB AR 31)")
        lbl_trans.setStyleSheet("font-size: 10px; font-weight: bold; color: #aaa;")
        v_trans.addWidget(lbl_trans)

        h_trans = QHBoxLayout()
        self.lbl_trans_status = QLabel("Bereit!")
        self.lbl_trans_status.setStyleSheet("font-size: 11px; font-weight: bold; color: #38e3e3;")
        h_trans.addWidget(self.lbl_trans_status)
        h_trans.addStretch()

        self.btn_trans_reset = QPushButton("Jetzt nutzen (7d)")
        self.btn_trans_reset.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_trans_reset.clicked.connect(self.reset_transformer_timer)
        h_trans.addWidget(self.btn_trans_reset)
        v_trans.addLayout(h_trans)

        self.grid_layout.addWidget(self.box_trans, 1, 1)

        # =========================================================================
        # Box 5: Artefakt-Routen-Timer (Freigeschaltet ab AR 45)
        # =========================================================================
        self.box_art = QFrame()
        self.box_art.setObjectName("sub_card")
        v_art = QVBoxLayout(self.box_art)
        v_art.setContentsMargins(10, 8, 10, 8)
        v_art.setSpacing(6)

        lbl_art = QLabel("ARTEFAKT-ROUTE (AB AR 45)")
        lbl_art.setStyleSheet("font-size: 10px; font-weight: bold; color: #aaa;")
        v_art.addWidget(lbl_art)

        h_art = QHBoxLayout()
        self.lbl_art_status = QLabel("Bereit zum Farmen!")
        self.lbl_art_status.setStyleSheet("font-size: 11px; font-weight: bold; color: #38e3e3;")
        h_art.addWidget(self.lbl_art_status)
        h_art.addStretch()

        self.btn_art_reset = QPushButton("Route gelaufen")
        self.btn_art_reset.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_art_reset.clicked.connect(self.reset_artifact_timer)
        h_art.addWidget(self.btn_art_reset)
        v_art.addLayout(h_art)

        self.grid_layout.addWidget(self.box_art, 2, 0)

        # =========================================================================
        # Box 6: Endgame Content (Abyss & Theater - Freigeschaltet ab AR 45)
        # =========================================================================
        self.box_endgame = QFrame()
        self.box_endgame.setObjectName("sub_card")
        v_endgame = QVBoxLayout(self.box_endgame)
        v_endgame.setContentsMargins(10, 8, 10, 8)
        v_endgame.setSpacing(6)

        lbl_endgame = QLabel("ENDGAME STERNE (AB AR 45)")
        lbl_endgame.setStyleSheet("font-size: 10px; font-weight: bold; color: #aaa;")
        v_endgame.addWidget(lbl_endgame)

        h_stars = QHBoxLayout()

        lbl_abyss = QLabel("Abgrund:")
        self.spin_abyss = QSpinBox()
        self.spin_abyss.setRange(0, 36)
        self.spin_abyss.valueChanged.connect(self.on_state_changed)

        lbl_theater = QLabel("Theater:")
        self.spin_theater = QSpinBox()
        self.spin_theater.setRange(0, 10)
        self.spin_theater.valueChanged.connect(self.on_state_changed)

        h_stars.addWidget(lbl_abyss)
        h_stars.addWidget(self.spin_abyss)
        h_stars.addSpacing(15)
        h_stars.addWidget(lbl_theater)
        h_stars.addWidget(self.spin_theater)
        h_stars.addStretch()

        v_endgame.addLayout(h_stars)

        self.grid_layout.addWidget(self.box_endgame, 2, 1)

        main_layout.addLayout(self.grid_layout)
        self.apply_theme_style()
        self.update_visibility_by_ar()

    def on_ar_changed(self):
        self.update_visibility_by_ar()
        self.on_state_changed()

    def update_visibility_by_ar(self):
        ar = self.spin_ar.value()

        # AR-Schwellenwerte steuern die Sichtbarkeit
        self.box_pot.setVisible(ar >= 28)
        self.box_trans.setVisible(ar >= 31)
        self.box_art.setVisible(ar >= 45)
        self.box_endgame.setVisible(ar >= 45)

    def reset_transformer_timer(self):
        self.transformer_end_time = time.time() + 604800
        self.update_timers()
        self.on_state_changed()

    def reset_artifact_timer(self):
        self.artifact_end_time = time.time() + 86400
        self.update_timers()
        self.on_state_changed()

    def update_timers(self):
        theme = get_theme()
        now = time.time()

        if self.transformer_end_time > now:
            rem = int(self.transformer_end_time - now)
            d = rem // 86400
            h = (rem % 86400) // 3600
            m = (rem % 3600) // 60
            self.lbl_trans_status.setText(f"In {d}d {h:02d}h {m:02d}m")
            self.lbl_trans_status.setStyleSheet("font-size: 11px; font-weight: bold; color: #ffaa00;")
        else:
            self.lbl_trans_status.setText("Bereit!")
            self.lbl_trans_status.setStyleSheet(f"font-size: 11px; font-weight: bold; color: {theme['cyan']};")

        if self.artifact_end_time > now:
            rem = int(self.artifact_end_time - now)
            h = rem // 3600
            m = (rem % 3600) // 60
            s = rem % 60
            self.lbl_art_status.setText(f"In {h:02d}h {m:02d}m {s:02d}s")
            self.lbl_art_status.setStyleSheet("font-size: 11px; font-weight: bold; color: #ffaa00;")
        else:
            self.lbl_art_status.setText("Bereit zum Farmen!")
            self.lbl_art_status.setStyleSheet(f"font-size: 11px; font-weight: bold; color: {theme['cyan']};")

    def get_today_rotation(self):
        weekday = datetime.today().weekday()
        if weekday in [0, 3]:
            return "Mo / Do: Freiheit, Wohlstand, Lehre, Versteck, Gleichmut"
        elif weekday in [1, 4]:
            return "Di / Fr: Widerstand, Gold, Ewigkeit, Einfachheit, Gerechtigkeit"
        elif weekday in [2, 5]:
            return "Mi / Sa: Ballade, Fleiß, Vergeltung, Praxis, Ordnung"
        else:
            return "🌟 Sonntag: Alle Sphären & Domänen sind offen!"

    def apply_theme_style(self):
        theme = get_theme()
        self.setStyleSheet(f"""
            TeyvatJournalWidget {{
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
            }}
            QCheckBox {{
                color: #e6e6e6;
                spacing: 6px;
                font-size: 11px;
                font-weight: bold;
            }}
            QCheckBox::indicator {{
                width: 14px;
                height: 14px;
                border-radius: 3px;
                border: 1px solid {theme['cyan']};
                background: {theme['bg_dark']};
            }}
            QCheckBox::indicator:checked {{
                background: {theme['cyan']};
            }}
            QPushButton {{
                background-color: #2a2e3a;
                color: {theme['cyan']};
                border: 1px solid {theme['cyan']};
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {theme['cyan']};
                color: #1a1c24;
            }}
            QSpinBox {{
                background-color: #2a2e3a;
                color: white;
                border: 1px solid {theme['cyan']};
                border-radius: 4px;
                padding: 2px 4px;
                font-size: 11px;
                font-weight: bold;
            }}
        """)
        self.rotation_label.setStyleSheet(f"color: {theme['amber']}; font-weight: bold; font-size: 10px;")
        self.update_timers()

    def on_state_changed(self):
        if self.parent_window and hasattr(self.parent_window, "save_expeditions"):
            self.parent_window.save_expeditions()

    def get_state_dict(self):
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "ar_level": self.spin_ar.value(),
            "commissions": [cb.isChecked() for cb in self.comm_boxes],
            "katheryne": self.katheryne_cb.isChecked(),
            "bosses": [cb.isChecked() for cb in self.boss_boxes],
            "transformer_end_time": self.transformer_end_time,
            "artifact_end_time": self.artifact_end_time,
            "pot_resin": self.pot_resin_cb.isChecked(),
            "pot_books": self.pot_books_cb.isChecked(),
            "pot_arte": self.pot_arte_cb.isChecked(),
            "abyss_stars": self.spin_abyss.value(),
            "theater_stars": self.spin_theater.value(),
        }

    def load_state_dict(self, data):
        if not data:
            return
        saved_date = data.get("date", "")
        today_str = datetime.now().strftime("%Y-%m-%d")
        is_today = saved_date == today_str

        # AR Level laden
        self.spin_ar.setValue(data.get("ar_level", 21))

        # Daily Reset
        comm_states = data.get("commissions", [False] * 4)
        for i, cb in enumerate(self.comm_boxes):
            cb.setChecked(comm_states[i] if is_today else False)

        self.katheryne_cb.setChecked(data.get("katheryne", False) if is_today else False)

        # Timers
        self.transformer_end_time = data.get("transformer_end_time", 0.0)
        self.artifact_end_time = data.get("artifact_end_time", 0.0)

        # Wöchentliches & Kannenreich
        boss_states = data.get("bosses", [False] * 3)
        for i, cb in enumerate(self.boss_boxes):
            cb.setChecked(boss_states[i])

        self.pot_resin_cb.setChecked(data.get("pot_resin", False))
        self.pot_books_cb.setChecked(data.get("pot_books", False))
        self.pot_arte_cb.setChecked(data.get("pot_arte", False))

        # Endgame Stars
        self.spin_abyss.setValue(data.get("abyss_stars", 0))
        self.spin_theater.setValue(data.get("theater_stars", 0))

        self.update_visibility_by_ar()
        self.update_timers()
