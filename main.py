import json
import os
import sys
import time

# --- WINDOWS SYSTEM-TRAY FIX ---
if sys.platform.startswith("win"):
    try:
        import ctypes
        myappid = "genshintracker.expedition.desktop.1"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except Exception:
        pass

try:
    from plyer import notification
except ImportError:
    notification = None

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QColor, QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QPushButton,
    QStackedWidget,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from config import (
    ASSETS_DIR,
    REGION_THEMES,
    SAVE_FILE,
    get_theme,
    is_autostart_enabled,
    set_active_theme,
    set_autostart,
)
from crafting import CraftingCalculatorWidget
from dialogs import InlineAddDialog, InlineResinDialog
from journal import TeyvatJournalWidget
from resin_planner import ResinPlannerWidget
from team_goals import TeamGoalsWidget
from weekly_bosses import WeeklyBossTrackerWidget
from widgets import ExpeditionCard, OperationsHQCard
from wishes import WishPityCounterWidget


class GenshinTrackerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Genshin Impact Expedition Tracker")
        self.current_theme_name = "Mondstadt (Anemo)"
        self.close_to_tray = True

        self.init_system_tray()

        # Main Central Widget with HORIZONTAL Layout (Sidebar + Content)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.root_layout = QHBoxLayout(self.central_widget)
        self.root_layout.setContentsMargins(0, 0, 0, 0)
        self.root_layout.setSpacing(0)

        # ---------------------------------------------------------------------
        # 1. VERTICAL SIDEBAR (LEFT)
        # ---------------------------------------------------------------------
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("sidebar_frame")
        self.sidebar_frame.setFixedWidth(64)
        self.sidebar_layout = QVBoxLayout(self.sidebar_frame)
        self.sidebar_layout.setContentsMargins(8, 12, 8, 12)
        self.sidebar_layout.setSpacing(12)

        # App Logo Header
        self.lbl_logo = QLabel("⚔️")
        self.lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_logo.setStyleSheet("font-size: 20px; margin-bottom: 8px;")
        self.sidebar_layout.addWidget(self.lbl_logo)

        # Navigation Buttons (Top to Bottom)
        self.btn_nav_expeditions = self.create_nav_button("⏳", "Expeditions")
        self.btn_nav_expeditions.clicked.connect(lambda: self.switch_page(0))
        self.sidebar_layout.addWidget(self.btn_nav_expeditions)

        self.btn_nav_journal = self.create_nav_button("📖", "Teyvat Journal")
        self.btn_nav_journal.clicked.connect(lambda: self.switch_page(1))
        self.sidebar_layout.addWidget(self.btn_nav_journal)

        self.btn_nav_crafting = self.create_nav_button("🧪", "Crafting Calculator")
        self.btn_nav_crafting.clicked.connect(lambda: self.switch_page(2))
        self.sidebar_layout.addWidget(self.btn_nav_crafting)

        self.btn_nav_wishes = self.create_nav_button("🌠", "Wish & Pity Counter")
        self.btn_nav_wishes.clicked.connect(lambda: self.switch_page(3))
        self.sidebar_layout.addWidget(self.btn_nav_wishes)

        self.btn_nav_resin = self.create_nav_button("⚡", "Resin Planner")
        self.btn_nav_resin.clicked.connect(lambda: self.switch_page(4))
        self.sidebar_layout.addWidget(self.btn_nav_resin)

        self.btn_nav_bosses = self.create_nav_button("🐲", "Weekly Boss Tracker")
        self.btn_nav_bosses.clicked.connect(lambda: self.switch_page(5))
        self.sidebar_layout.addWidget(self.btn_nav_bosses)

        self.btn_nav_team = self.create_nav_button("🎯", "Team & Farming Goals")
        self.btn_nav_team.clicked.connect(lambda: self.switch_page(6))
        self.sidebar_layout.addWidget(self.btn_nav_team)

        self.sidebar_layout.addStretch()

        # Settings Button (Fixed at Bottom)
        self.btn_nav_settings = self.create_nav_button("⚙️", "Settings")
        self.btn_nav_settings.clicked.connect(lambda: self.switch_page(7))
        self.sidebar_layout.addWidget(self.btn_nav_settings)

        self.root_layout.addWidget(self.sidebar_frame)

        # ---------------------------------------------------------------------
        # 2. MAIN CONTENT AREA WITH STACKED WIDGET (RIGHT)
        # ---------------------------------------------------------------------
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(16, 16, 16, 16)
        self.content_layout.setSpacing(10)

        # Header Bar
        header_layout = QHBoxLayout()
        self.lbl_page_title = QLabel("Active Expeditions")
        self.lbl_page_title.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        header_layout.addWidget(self.lbl_page_title)

        header_layout.addStretch()

        lbl_theme = QLabel("Theme:")
        lbl_theme.setStyleSheet("font-size: 12px; font-weight: bold; color: #aaa;")
        header_layout.addWidget(lbl_theme)

        self.combo_theme = QComboBox()
        self.combo_theme.addItems(list(REGION_THEMES.keys()))
        self.combo_theme.setCurrentText(self.current_theme_name)
        self.combo_theme.currentTextChanged.connect(self.apply_theme)
        header_layout.addWidget(self.combo_theme)

        self.content_layout.addLayout(header_layout)

        # STACKED WIDGET FOR PAGE SWITCHING
        self.stacked_widget = QStackedWidget()

        # PAGE 0: Expeditions Grid
        self.page_expeditions = QWidget()
        v_exp_layout = QVBoxLayout(self.page_expeditions)
        v_exp_layout.setContentsMargins(0, 10, 0, 0)

        self.cards_grid = QGridLayout()
        self.cards_grid.setContentsMargins(0, 0, 0, 0)
        self.cards_grid.setSpacing(12)

        for col in range(3):
            self.cards_grid.setColumnStretch(col, 1)
        for row in range(2):
            self.cards_grid.setRowStretch(row, 1)

        v_exp_layout.addLayout(self.cards_grid, stretch=1)
        v_exp_layout.addSpacing(10)

        self.btn_start_new = QPushButton()
        self.btn_start_new.clicked.connect(self.open_add_dialog)
        v_exp_layout.addWidget(self.btn_start_new)

        self.stacked_widget.addWidget(self.page_expeditions)

        # PAGE 1: Teyvat Journal
        self.journal_widget = TeyvatJournalWidget(parent_window=self)
        self.stacked_widget.addWidget(self.journal_widget)

        # PAGE 2: Crafting Calculator
        self.crafting_widget = CraftingCalculatorWidget(parent_window=self)
        self.stacked_widget.addWidget(self.crafting_widget)

        # PAGE 3: Wish & Pity Counter
        self.wishes_widget = WishPityCounterWidget(parent_window=self)
        self.stacked_widget.addWidget(self.wishes_widget)

        # PAGE 4: Resin Planner
        self.resin_widget = ResinPlannerWidget(parent_window=self)
        self.stacked_widget.addWidget(self.resin_widget)

        # PAGE 5: Weekly Boss Tracker
        self.bosses_widget = WeeklyBossTrackerWidget(parent_window=self)
        self.stacked_widget.addWidget(self.bosses_widget)

        # PAGE 6: Team & Farming Goals
        self.team_widget = TeamGoalsWidget(parent_window=self)
        self.stacked_widget.addWidget(self.team_widget)

        # PAGE 7: Settings Page
        self.page_settings = self.create_settings_page()
        self.stacked_widget.addWidget(self.page_settings)

        self.content_layout.addWidget(self.stacked_widget, stretch=1)
        self.root_layout.addWidget(self.content_container, stretch=1)

        # State & Timer Initialization
        self.active_cards = []
        self.overlay_dialog = None
        self.hq_card = OperationsHQCard(parent_window=self)

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.on_timer_tick)
        self.update_timer.start(1000)

        self.load_expeditions()
        self.apply_theme(self.current_theme_name)
        self.switch_page(0)  # Default page: Expeditions

        self.setMinimumSize(1280, 850)
        self.resize(1280, 850)

    def create_nav_button(self, icon_str, tooltip):
        btn = QPushButton(icon_str)
        btn.setFixedSize(44, 44)
        btn.setToolTip(tooltip)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        return btn

    def switch_page(self, index):
        self.stacked_widget.setCurrentIndex(index)
        titles = [
            "Active Expeditions",
            "Teyvat Journal & HQ Operations",
            "Alchemy & Crafting Bench Calculator",
            "Wish & Pity Savings Counter",
            "Original Resin Overflow & Cap Planner",
            "Weekly Boss Discount & Claim Tracker",
            "Team Building & Farming Goals",
            "Settings & Preferences",
        ]
        self.lbl_page_title.setText(titles[index])
        self.update_nav_styles(index)

    def update_nav_styles(self, active_index):
        theme = get_theme()
        buttons = [
            self.btn_nav_expeditions,
            self.btn_nav_journal,
            self.btn_nav_crafting,
            self.btn_nav_wishes,
            self.btn_nav_resin,
            self.btn_nav_bosses,
            self.btn_nav_team,
            self.btn_nav_settings,
        ]

        for i, btn in enumerate(buttons):
            if i == active_index:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {theme['cyan']};
                        color: #1a1c24;
                        border: none;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: bold;
                    }}
                """)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: #1a1c24;
                        color: #ffffff;
                        border: 1px solid #3d4254;
                        border-radius: 8px;
                        font-size: 18px;
                    }}
                    QPushButton:hover {{
                        border-color: {theme['cyan']};
                        color: {theme['cyan']};
                    }}
                """)

    def create_settings_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        card = QFrame()
        card.setObjectName("settings_card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)

        lbl_sec = QLabel("System Settings")
        lbl_sec.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        card_layout.addWidget(lbl_sec)

        self.chk_autostart = QCheckBox("Start with System (Autostart)")
        self.chk_autostart.setChecked(is_autostart_enabled())
        self.chk_autostart.stateChanged.connect(self.on_settings_changed)
        card_layout.addWidget(self.chk_autostart)

        lbl_close = QLabel("Window Close Behavior (✕):")
        lbl_close.setStyleSheet("font-size: 12px; font-weight: bold; color: #aaa;")
        card_layout.addWidget(lbl_close)

        self.combo_close_action = QComboBox()
        self.combo_close_action.addItem("Minimize to System Tray", userData=True)
        self.combo_close_action.addItem("Exit Application Completely", userData=False)
        self.combo_close_action.currentIndexChanged.connect(self.on_settings_changed)
        card_layout.addWidget(self.combo_close_action)

        card_layout.addStretch()
        layout.addWidget(card)
        layout.addStretch()

        return page

    def on_settings_changed(self):
        autostart = self.chk_autostart.isChecked()
        close_to_tray = self.combo_close_action.currentData()
        set_autostart(autostart)
        self.close_to_tray = close_to_tray if close_to_tray is not None else True
        self.save_expeditions()

    def apply_theme(self, theme_name):
        self.current_theme_name = theme_name
        set_active_theme(theme_name)
        theme = get_theme()

        self.setStyleSheet(f"""
            QMainWindow {{ background-color: {theme['bg_dark']}; }}
            QWidget {{ color: #e6e6e6; font-family: 'Segoe UI', sans-serif; }}
            QFrame#sidebar_frame {{
                background-color: #15171e;
                border-right: 1px solid #2d313e;
            }}
            QFrame#settings_card {{
                background-color: {theme['card_bg']};
                border: 1px solid #333847;
                border-radius: 12px;
            }}
            QComboBox {{
                background-color: #1a1c24;
                color: white;
                border: 1px solid {theme['cyan']};
                border-radius: 5px;
                padding: 4px 8px;
                font-size: 12px;
            }}
        """)

        self.update_nav_styles(self.stacked_widget.currentIndex())

        if hasattr(self, "hq_card"):
            self.hq_card.apply_theme_style()
            self.hq_card.update_info()

        if hasattr(self, "journal_widget"):
            self.journal_widget.apply_theme_style()

        if hasattr(self, "crafting_widget"):
            self.crafting_widget.apply_theme_style()
            self.crafting_widget.calculate()

        if hasattr(self, "wishes_widget"):
            self.wishes_widget.apply_theme_style()
            self.wishes_widget.calculate()

        if hasattr(self, "resin_widget"):
            self.resin_widget.apply_theme_style()
            self.resin_widget.calculate()

        if hasattr(self, "bosses_widget"):
            self.bosses_widget.apply_theme_style()
            self.bosses_widget.update_summary()

        if hasattr(self, "team_widget"):
            self.team_widget.apply_theme_style()
            self.team_widget.update_summary()

        for card in self.active_cards:
            card.style_card(active=card.get_remaining_seconds() > 0)
            card.ring_timer.update()

        self.update_add_button_state()
        self.save_expeditions()

    def init_system_tray(self):
        self.tray_icon = QSystemTrayIcon(self)

        icon_path = os.path.join(ASSETS_DIR, "traveler.png")

        if os.path.exists(icon_path):
            app_icon = QIcon(icon_path)
        else:
            app_icon = QIcon.fromTheme("applications-games", QIcon.fromTheme("clock"))
            if app_icon.isNull():
                pixmap = QPixmap(32, 32)
                pixmap.fill(QColor(get_theme()["cyan"]))
                app_icon = QIcon(pixmap)

        self.setWindowIcon(app_icon)
        self.tray_icon.setIcon(app_icon)

        tray_menu = QMenu()
        action_show = QAction("Open Tracker", self)
        action_show.triggered.connect(self.show_normal)
        tray_menu.addAction(action_show)

        tray_menu.addSeparator()

        action_quit = QAction("Quit", self)
        action_quit.triggered.connect(self.quit_application)
        tray_menu.addAction(action_quit)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.tray_icon.show()

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.show_normal()

    def show_normal(self):
        self.show()
        self.setWindowState(Qt.WindowState.WindowActive)
        self.raise_()

    def closeEvent(self, event):
        if self.close_to_tray and self.tray_icon.isSystemTrayAvailable():
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "Genshin Tracker",
                "Running in background.",
                QSystemTrayIcon.MessageIcon.Information,
                2000,
            )
        else:
            event.accept()
            self.quit_application()

    def quit_application(self):
        self.tray_icon.hide()
        QApplication.quit()

    def update_add_button_state(self):
        theme = get_theme()
        count = len(self.active_cards)
        max_limit = 5

        if count >= max_limit:
            self.btn_start_new.setEnabled(False)
            self.btn_start_new.setText(f"Limit Reached ({count}/{max_limit} Expeditions)")
            self.btn_start_new.setCursor(Qt.CursorShape.ForbiddenCursor)
            self.btn_start_new.setStyleSheet("""
                QPushButton {
                    background-color: #1e2029;
                    border: 2px solid #333745;
                    border-radius: 8px;
                    padding: 10px;
                    font-size: 13px;
                    font-weight: bold;
                    color: #555866;
                }
            """)
        else:
            self.btn_start_new.setEnabled(True)
            self.btn_start_new.setText(f"+ Start New Expedition ({count}/{max_limit})")
            self.btn_start_new.setCursor(Qt.CursorShape.PointingHandCursor)
            self.btn_start_new.setStyleSheet(f"""
                QPushButton {{
                    background-color: {theme['card_bg']};
                    border: 2px solid #444;
                    border-radius: 8px;
                    padding: 10px;
                    font-size: 13px;
                    font-weight: bold;
                    color: #888;
                }}
                QPushButton:hover {{
                    border-color: {theme['cyan']};
                    color: {theme['cyan']};
                    background-color: #2a2e3a;
                }}
            """)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.position_overlay()

    def position_overlay(self):
        if self.overlay_dialog:
            cw = self.central_widget
            x = (cw.width() - self.overlay_dialog.width()) // 2
            y = (cw.height() - self.overlay_dialog.height()) // 2
            self.overlay_dialog.move(max(0, x), max(0, y))

    def open_add_dialog(self):
        if len(self.active_cards) >= 5 or self.overlay_dialog:
            return

        self.overlay_dialog = InlineAddDialog(
            parent=self.central_widget,
            on_submit=self.on_dialog_submit,
            on_cancel=self.close_overlay,
        )
        self.overlay_dialog.show()
        self.overlay_dialog.raise_()
        self.position_overlay()

    def open_resin_dialog(self):
        if self.overlay_dialog:
            return

        self.overlay_dialog = InlineResinDialog(
            current_resin=self.hq_card.current_resin,
            max_resin=self.hq_card.max_resin,
            on_submit=self.on_resin_submit,
            on_cancel=self.close_overlay,
            parent=self.central_widget,
        )
        self.overlay_dialog.show()
        self.overlay_dialog.raise_()
        self.position_overlay()

    def on_dialog_submit(self, char, loc, hours):
        self.create_card(char, loc, hours * 3600)
        self.close_overlay()
        self.save_expeditions()

    def on_resin_submit(self, new_resin_val):
        self.hq_card.current_resin = new_resin_val
        self.hq_card.last_resin_update = time.time()
        self.hq_card.update_info()

        if hasattr(self, "resin_widget"):
            self.resin_widget.spin_resin.setValue(new_resin_val)

        self.save_expeditions()
        self.close_overlay()

    def close_overlay(self):
        if self.overlay_dialog:
            self.overlay_dialog.deleteLater()
            self.overlay_dialog = None

    def create_card(self, char, loc, total_seconds, end_timestamp=None):
        card = ExpeditionCard(
            char,
            loc,
            total_seconds,
            end_timestamp=end_timestamp,
            on_delete=self.remove_card,
            parent=self,
        )
        self.active_cards.append(card)
        self.regrid_cards()

    def remove_card(self, card_to_remove):
        if card_to_remove in self.active_cards:
            self.cards_grid.removeWidget(card_to_remove)
            self.active_cards.remove(card_to_remove)
            card_to_remove.deleteLater()
            self.regrid_cards()
            self.save_expeditions()

    def regrid_cards(self):
        for i in reversed(range(self.cards_grid.count())):
            widget = self.cards_grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for i, card in enumerate(self.active_cards):
            row = i // 3
            col = i % 3
            self.cards_grid.addWidget(card, row, col)

        hq_index = len(self.active_cards)
        hq_row = hq_index // 3
        hq_col = hq_index % 3
        self.cards_grid.addWidget(self.hq_card, hq_row, hq_col)

        self.update_add_button_state()
        self.hq_card.update_info()

    def on_timer_tick(self):
        for card in self.active_cards:
            just_finished = card.update_time()
            if just_finished:
                msg = f"The expedition of {card.char_name} has finished!"
                if notification:
                    try:
                        notification.notify(
                            title="Genshin Impact Tracker",
                            message=msg,
                            app_name="GenshinTimer",
                            timeout=5,
                        )
                    except Exception:
                        pass
                if self.tray_icon.isSystemTrayAvailable():
                    self.tray_icon.showMessage(
                        "Expedition Complete",
                        msg,
                        QSystemTrayIcon.MessageIcon.Information,
                        5000,
                    )

        if hasattr(self, "journal_widget"):
            self.journal_widget.update_timers()

        self.hq_card.update_info()

    def save_expeditions(self):
        data = {
            "last_modified": int(time.time()),
            "expeditions": [card.to_dict() for card in self.active_cards],
            "resin": self.hq_card.current_resin,
            "last_resin_update": self.hq_card.last_resin_update,
            "theme": self.current_theme_name,
            "close_to_tray": self.close_to_tray,
            "teyvat_journal": self.journal_widget.get_state_dict() if hasattr(self, "journal_widget") else {},
            "wishes": self.wishes_widget.get_state_dict() if hasattr(self, "wishes_widget") else {},
            "weekly_bosses": self.bosses_widget.get_state_dict() if hasattr(self, "bosses_widget") else {},
            "team_goals": self.team_widget.get_state_dict() if hasattr(self, "team_widget") else [],
        }
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving: {e}")

    def load_expeditions(self):
        if not os.path.exists(SAVE_FILE):
            self.regrid_cards()
            return
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

                if isinstance(data, dict):
                    expeditions = data.get("expeditions", [])
                    self.hq_card.current_resin = data.get("resin", 120)
                    self.hq_card.last_resin_update = data.get("last_resin_update", time.time())
                    self.current_theme_name = data.get("theme", "Mondstadt (Anemo)")
                    self.close_to_tray = data.get("close_to_tray", True)

                    idx = 0 if self.close_to_tray else 1
                    self.combo_close_action.setCurrentIndex(idx)

                    if hasattr(self, "journal_widget"):
                        self.journal_widget.load_state_dict(data.get("teyvat_journal", {}))
                    if hasattr(self, "wishes_widget"):
                        self.wishes_widget.load_state_dict(data.get("wishes", {}))
                    if hasattr(self, "bosses_widget"):
                        self.bosses_widget.load_state_dict(data.get("weekly_bosses", {}))
                    if hasattr(self, "team_widget"):
                        self.team_widget.load_state_dict(data.get("team_goals", []))
                else:
                    expeditions = data

                for item in expeditions:
                    self.create_card(
                        item["char_name"],
                        item["location"],
                        item["total_seconds"],
                        end_timestamp=item["end_timestamp"],
                    )
                if hasattr(self, "combo_theme"):
                    self.combo_theme.setCurrentText(self.current_theme_name)

        except Exception as e:
            print(f"Error loading: {e}")


if __name__ == "__main__":
    QApplication.setDesktopFileName("genshin-expedition-tracker")
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    window = GenshinTrackerWindow()
    window.show()

    sys.exit(app.exec())
