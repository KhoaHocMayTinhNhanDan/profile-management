import os
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from ..level_01_atoms.buttons import NavButton

class Sidebar(QFrame):
    """
    Sidebar - Thanh điều hướng bên trái ứng dụng.
    Toàn bộ style được định nghĩa tập trung trong QSS của ThemeManager.
    """
    def __init__(self, root_dir, i18n_manager, nav_callback, parent=None):
        super().__init__(parent)
        self.i18n_manager = i18n_manager
        self.setObjectName("sidebar")  # Trùng khớp với selector QFrame#sidebar của QSS
        self.setFixedWidth(240)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 25, 15, 25)
        layout.setSpacing(12)
        
        # Logo/Brand
        brand_container = QWidget()
        brand_layout = QVBoxLayout(brand_container)
        brand_layout.setContentsMargins(5, 0, 5, 15)
        
        self.logo = QLabel("🏛️ CLEAN ARCH")
        self.logo.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        self.logo.setProperty("class", "HeaderLabel")
        
        self.sub_logo = QLabel("Project Scaffolder")
        self.sub_logo.setFont(QFont("Inter", 10, QFont.Weight.Medium))
        self.sub_logo.setProperty("class", "BodyLabel")
        
        brand_layout.addWidget(self.logo)
        brand_layout.addWidget(self.sub_logo)
        layout.addWidget(brand_container)
        
        # Navigation Buttons Group
        self.nav_buttons = []
        self.nav_items_meta = [
            ("Dashboard", 0, "📊 "),
            ("Add Feature", 1, "➕ "),
            ("Check Architecture", 2, "🛡️ "),
            ("Backup / Restore", 3, "💾 "),
            ("Danger Zone", 4, "⚠️ ")
        ]
        
        for key, index, emoji in self.nav_items_meta:
            btn = NavButton("")
            btn.clicked.connect(lambda checked, idx=index: nav_callback(idx))
            layout.addWidget(btn)
            self.nav_buttons.append(btn)
            
        self.nav_buttons[0].setChecked(True)  # Mặc định kích hoạt Dashboard
        
        layout.addStretch()
        
        # --- Settings Panel (Theme & Language) ---
        settings_container = QFrame()
        settings_container.setObjectName("settings_container")
        settings_layout = QVBoxLayout(settings_container)
        settings_layout.setSpacing(6)
        
        # Language Selector
        lang_layout = QHBoxLayout()
        self.lbl_lang = QLabel("Language:")
        self.lbl_lang.setFont(QFont("Inter", 8, QFont.Weight.Bold))
        self.lbl_lang.setProperty("class", "BodyLabel")
        
        self.combo_lang = QComboBox()
        self.avail_langs = self.i18n_manager.get_available_languages()
        self.lang_codes = list(self.avail_langs.keys())
        self.combo_lang.addItems(list(self.avail_langs.values()))
        self.combo_lang.currentIndexChanged.connect(self.handle_lang_change)
        
        lang_layout.addWidget(self.lbl_lang)
        lang_layout.addWidget(self.combo_lang)
        settings_layout.addLayout(lang_layout)
        
        # Theme Selector
        theme_layout = QHBoxLayout()
        self.lbl_theme = QLabel("Theme:")
        self.lbl_theme.setFont(QFont("Inter", 8, QFont.Weight.Bold))
        self.lbl_theme.setProperty("class", "BodyLabel")
        
        self.combo_theme = QComboBox()
        self.combo_theme.addItems(["Classic", "Comic", "Galaxy", "Ironman"])
        self.combo_theme.currentIndexChanged.connect(self.handle_theme_change)
        
        theme_layout.addWidget(self.lbl_theme)
        theme_layout.addWidget(self.combo_theme)
        settings_layout.addLayout(theme_layout)
        
        # Mode Selector (Light/Dark Mode)
        mode_layout = QHBoxLayout()
        self.lbl_mode = QLabel("Mode:")
        self.lbl_mode.setFont(QFont("Inter", 8, QFont.Weight.Bold))
        self.lbl_mode.setProperty("class", "BodyLabel")
        
        self.combo_mode = QComboBox()
        self.combo_mode.addItems(["Dark Mode", "Light Mode"])
        self.combo_mode.currentIndexChanged.connect(self.handle_mode_change)
        
        mode_layout.addWidget(self.lbl_mode)
        mode_layout.addWidget(self.combo_mode)
        settings_layout.addLayout(mode_layout)
        
        layout.addWidget(settings_container)
        
        # --- Workspace Path Label at Bottom of Sidebar ---
        path_container = QFrame()
        path_container.setObjectName("path_container")
        path_layout = QVBoxLayout(path_container)
        path_layout.setContentsMargins(5, 5, 5, 5)
        
        self.path_title = QLabel("WORKSPACE ROOT")
        self.path_title.setFont(QFont("Inter", 8, QFont.Weight.Bold))
        self.path_title.setProperty("class", "BodyLabel")
        
        self.path_val = QLabel(os.path.basename(root_dir))
        self.path_val.setFont(QFont("Inter", 9, QFont.Weight.Bold))
        self.path_val.setProperty("class", "HeaderLabel")
        
        path_layout.addWidget(self.path_title)
        path_layout.addWidget(self.path_val)
        layout.addWidget(path_container)
        
        # Áp dụng trạng thái ngôn ngữ mặc định
        self.retranslate_ui()
        self.i18n_manager.language_changed.connect(self.retranslate_ui)

    def handle_lang_change(self, index):
        if 0 <= index < len(self.lang_codes):
            lang_code = self.lang_codes[index]
            self.i18n_manager.switch_language(lang_code)

    def handle_theme_change(self, index):
        themes = ["classic", "comic", "galaxy", "ironman"]
        selected_theme = themes[index]
        win = self.window()
        if hasattr(win, "app_ctx"):
            win.app_ctx.theme_manager.switch_theme(selected_theme)

    def handle_mode_change(self, index):
        mode = "dark" if index == 0 else "light"
        win = self.window()
        if hasattr(win, "app_ctx"):
            win.app_ctx.mode_manager.switch_mode(mode)

    def retranslate_ui(self):
        for idx, (key, index, emoji) in enumerate(self.nav_items_meta):
            translated = self.i18n_manager.translate(key)
            self.nav_buttons[idx].setText(f"{emoji}{translated}")
        
        self.lbl_lang.setText(self.i18n_manager.translate("Language") + ":")
        self.lbl_theme.setText(self.i18n_manager.translate("Theme") + ":")
        self.lbl_mode.setText(self.i18n_manager.translate("Mode") + ":")
        self.path_title.setText(self.i18n_manager.translate("Workspace Path") + ":")
        
        # Translate mode items dynamically
        self.combo_mode.blockSignals(True)
        current_idx = self.combo_mode.currentIndex()
        self.combo_mode.clear()
        self.combo_mode.addItems([
            self.i18n_manager.translate("Dark Mode"),
            self.i18n_manager.translate("Light Mode")
        ])
        self.combo_mode.setCurrentIndex(current_idx)
        self.combo_mode.blockSignals(False)

        # Translate theme items dynamically
        self.combo_theme.blockSignals(True)
        current_theme_idx = self.combo_theme.currentIndex()
        self.combo_theme.clear()
        self.combo_theme.addItems([
            self.i18n_manager.translate("Classic"),
            self.i18n_manager.translate("Comic"),
            self.i18n_manager.translate("Galaxy"),
            self.i18n_manager.translate("Ironman")
        ])
        self.combo_theme.setCurrentIndex(current_theme_idx)
        self.combo_theme.blockSignals(False)

        # Translate language items dynamically
        self.combo_lang.blockSignals(True)
        current_lang_code = self.i18n_manager.get_current_lang()
        self.avail_langs = self.i18n_manager.get_available_languages()
        self.lang_codes = list(self.avail_langs.keys())
        self.combo_lang.clear()
        self.combo_lang.addItems(list(self.avail_langs.values()))
        if current_lang_code in self.lang_codes:
            self.combo_lang.setCurrentIndex(self.lang_codes.index(current_lang_code))
        self.combo_lang.blockSignals(False)
        
    def select_button(self, index):
        for idx, btn in enumerate(self.nav_buttons):
            btn.setChecked(idx == index)
