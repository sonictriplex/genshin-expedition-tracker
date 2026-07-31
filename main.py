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
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMenu,
    QPushButton,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)

from config import (
    ASSETS_DIR,
    REGION_THEMES,
    SAVE_FILE,
    get_theme,
    set_active_theme,
    set_autostart,
)
from dialogs import InlineAddDialog, InlineResinDialog, InlineSettingsDialog
from widgets import ExpeditionCard, OperationsHQCard


class GenshinTrackerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Genshin Impact Expedition Tracker")
        self.current_theme_name = "Mondstadt (Anemo)"
        self.close_to_tray = True  # Standard-Verhalten beim Schließen

        self.init_system_tray()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(16, 16, 16, 16)

        # Header
        header_layout = QHBoxLayout()
        lbl_title = QLabel("Active Expeditions")
        lbl_title.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        header_layout.addWidget(lbl_title)
        header_layout.addStretch()

        lbl_theme = QLabel("Theme:")
        lbl_theme.setStyleSheet("font-size: 12px; font-weight: bold; color: #aaa;")
        header_layout.addWidget(lbl_theme)

        self.combo_theme = QComboBox()
        self.combo_theme.addItems(list(REGION_THEMES.keys()))
        self.combo_theme.setCurrentText(self.current_theme_name)
        self.combo_theme.currentTextChanged.connect(self.apply_theme)
        header_layout.addWidget(self.combo_theme)

        self.btn_menu = QPushButton("☰")
        self.btn_menu.setObjectName("btn_menu")
        self.btn_menu.setFixedSize(32, 32)
        self.btn_menu.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_menu.clicked.connect(self.show_hamburger_menu)
        header_layout.addWidget(self.btn_menu)

        self.main_layout.addLayout(header_layout)
        self.main_layout.addSpacing(10)

        # Grid
        self.grid_widget = QWidget()
        self.cards_grid = QGridLayout(self.grid_widget)
        self.cards_grid.setContentsMargins(0, 0, 0, 0)
        self.cards_grid.setSpacing(12)

        for col in range(3):
            self.cards_grid.setColumnStretch(col, 1)
        for row in range(2):
            self.cards_grid.setRowStretch(row, 1)

        self.main_layout.addWidget(self.grid_widget, stretch=1)
        self.main_layout.addSpacing(10)

        self.btn_start_new = QPushButton()
        self.btn_start_new.clicked.connect(self.open_add_dialog)
        self.main_layout.addWidget(self.btn_start_new)

        self.active_cards = []
        self.overlay_dialog = None
        self.hq_card = OperationsHQCard(parent_window=self)

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.on_timer_tick)
        self.update_timer.start(1000)

        self.load_expeditions()
        self.apply_theme(self.current_theme_name)
        self.update_add_button_state()

        self.setMinimumSize(1500, 975)
        self.resize(1500, 975)

    def init_system_tray(self):
        self.tray_icon = QSystemTrayIcon(self)

        # Sichere Icon-Kette für Windows & Linux/CachyOS
        icon_path_1 = os.path.join(ASSETS_DIR, "traveler.png")

        if os.path.exists(icon_path_1):
            app_icon = QIcon(icon_path_1)
        elif os.path.exists(icon_path_2):
            app_icon = QIcon(icon_path_2)
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

    def show_hamburger_menu(self):
        theme = get_theme()
        menu = QMenu(self)
        menu.setStyleSheet(f"""
            QMenu {{
                background-color: {theme['card_bg']};
                color: white;
                border: 1px solid #3d4254;
                border-radius: 6px;
                padding: 4px;
            }}
            QMenu::item {{
                padding: 8px 20px;
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: {theme['cyan']};
                color: #1a1c24;
                font-weight: bold;
            }}
        """)

        action_settings = QAction("⚙️ Settings", self)
        action_settings.triggered.connect(self.open_settings_dialog)
        menu.addAction(action_settings)

        btn_pos = self.btn_menu.mapToGlobal(self.btn_menu.rect().bottomLeft())
        menu.exec(btn_pos)

    def open_settings_dialog(self):
        if self.overlay_dialog:
            return

        self.overlay_dialog = InlineSettingsDialog(
            close_to_tray=self.close_to_tray,
            on_submit=self.on_settings_submit,
            on_cancel=self.close_overlay,
            parent=self.central_widget,
        )
        self.overlay_dialog.show()
        self.overlay_dialog.raise_()
        self.position_overlay()

    def on_settings_submit(self, autostart_enabled, close_to_tray_enabled):
        set_autostart(autostart_enabled)
        self.close_to_tray = close_to_tray_enabled
        self.save_expeditions()
        self.close_overlay()

    def apply_theme(self, theme_name):
        self.current_theme_name = theme_name
        set_active_theme(theme_name)
        theme = get_theme()

        self.setStyleSheet(f"""
            QMainWindow {{ background-color: {theme['bg_dark']}; }}
            QWidget {{ color: #e6e6e6; font-family: 'Segoe UI', sans-serif; }}
            QComboBox {{
                background-color: #1a1c24;
                color: white;
                border: 1px solid {theme['cyan']};
                border-radius: 5px;
                padding: 4px 8px;
                font-size: 12px;
            }}
            QPushButton#btn_menu {{
                background-color: {theme['card_bg']};
                color: {theme['cyan']};
                border: 1px solid #3d4254;
                border-radius: 5px;
                font-weight: bold;
            }}
        """)

        if hasattr(self, "hq_card"):
            self.hq_card.apply_theme_style()
            self.hq_card.update_info()

        for card in self.active_cards:
            card.style_card(active=card.get_remaining_seconds() > 0)
            card.ring_timer.update()

        self.update_add_button_state()
        self.save_expeditions()

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

        self.hq_card.update_info()

    def save_expeditions(self):
        data = {
            "expeditions": [card.to_dict() for card in self.active_cards],
            "resin": self.hq_card.current_resin,
            "last_resin_update": self.hq_card.last_resin_update,
            "theme": self.current_theme_name,
            "close_to_tray": self.close_to_tray,
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
