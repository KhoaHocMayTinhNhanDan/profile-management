# Template files for UI Presentation Services (Theme, i18n, Mode, BasePage)
# Đã được tách rời hoàn toàn khỏi PyQt6 (Framework-Agnostic) để sử dụng chung cho Web và Mobile.

I18N_MANAGER_TEMPLATE = '''import os
import json

class I18nManager:
    """
    Dịch vụ quản lý Đa ngôn ngữ (i18n) động thuần Python.
    Tải từ điển dịch thuật từ các file JSON tương ứng trong thư mục /locales/ khi đổi ngôn ngữ.
    """
    def __init__(self, current_lang: str = "en"):
        self._current_lang = current_lang
        self._dictionary = {}
        self._listeners = []
        self._load_translations(current_lang)

    def subscribe(self, callback):
        """Đăng ký callback nhận thông báo khi ngôn ngữ thay đổi."""
        self._listeners.append(callback)
        # Gửi ngôn ngữ hiện tại ngay khi subscribe để UI cập nhật lần đầu
        try:
            callback(self._current_lang)
        except Exception:
            pass

    def unsubscribe(self, callback):
        if callback in self._listeners:
            self._listeners.remove(callback)

    def get_current_lang(self) -> str:
        return self._current_lang

    def get_available_languages(self) -> dict:
        langs = {}
        # Tìm locales trong thư mục locales của i18n
        locales_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "locales")
        if os.path.exists(locales_dir):
            for file in os.listdir(locales_dir):
                if file.endswith(".json"):
                    lang_code = file[:-5]
                    json_path = os.path.join(locales_dir, file)
                    try:
                        with open(json_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            langs[lang_code] = data.get("LanguageName", lang_code)
                    except Exception:
                        langs[lang_code] = lang_code
        sorted_langs = {}
        if "en" in langs:
            sorted_langs["en"] = langs["en"]
        for code, name in sorted(langs.items()):
            if code != "en":
                sorted_langs[code] = name
        return sorted_langs

    def _load_translations(self, lang_code: str):
        self._dictionary = {}
        locales_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "locales")
        json_path = os.path.join(locales_dir, f"{lang_code}.json")
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    self._dictionary = json.load(f)
            except Exception as e:
                print(f"[I18nManager] Lỗi đọc file ngôn ngữ {lang_code}: {e}")

    def switch_language(self, lang_code: str):
        self._current_lang = lang_code
        self._load_translations(lang_code)
        for callback in self._listeners:
            try:
                callback(lang_code)
            except Exception as e:
                print(f"[I18nManager] Lỗi gọi callback: {e}")

    def translate(self, text: str, **kwargs) -> str:
        translated = self._dictionary.get(text, text)
        if kwargs:
            try:
                return translated.format(**kwargs)
            except Exception:
                pass
        return translated
'''

LIGHT_DARK_MODE_MANAGER_TEMPLATE = '''class LightDarkModeManager:
    """
    Dịch vụ quản lý Chế độ Sáng/Tối (Light/Dark Mode) thuần Python.
    Quản lý trạng thái "sáng" hoặc "tối" (light/dark) độc lập với Style Theme.
    """
    def __init__(self, default_mode: str = "dark"):
        self._current_mode = default_mode if default_mode in ["light", "dark"] else "dark"
        self._listeners = []

    def subscribe(self, callback):
        self._listeners.append(callback)
        try:
            callback(self._current_mode)
        except Exception:
            pass

    def unsubscribe(self, callback):
        if callback in self._listeners:
            self._listeners.remove(callback)

    def get_current_mode(self) -> str:
        return self._current_mode

    def is_dark(self) -> bool:
        return self._current_mode == "dark"

    def switch_mode(self, mode: str):
        if mode not in ["light", "dark"]:
            return
        if self._current_mode != mode:
            self._current_mode = mode
            for callback in self._listeners:
                try:
                    callback(mode)
                except Exception as e:
                    print(f"[LightDarkModeManager] Lỗi gọi callback: {e}")
'''

THEME_MANAGER_TEMPLATE = '''import os
import json

class ThemeManager:
    """
    ThemeManager - Dịch vụ quản lý Theme cắm-rút động (Plug-and-Play) thuần Python.
    Tự động quét cấu hình và trả về thông số QSS/màu sắc đã biên dịch.
    """
    def __init__(self, mode_manager, default_theme: str = "classic"):
        self.mode_manager = mode_manager
        
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.themes_dir = os.path.join(self.base_dir, "themes")
        self.qss_path = os.path.join(self.base_dir, "base.qss")
        
        self.palettes = {}
        self._listeners = []
        
        self.load_available_themes()
        self._current_theme = default_theme if default_theme in self.palettes else "classic"
        
        self.mode_manager.subscribe(self._handle_mode_change)

    def subscribe(self, callback):
        self._listeners.append(callback)
        try:
            callback(self._current_theme, self.get_formatted_qss())
        except Exception:
            pass

    def unsubscribe(self, callback):
        if callback in self._listeners:
            self._listeners.remove(callback)

    def load_available_themes(self):
        self.palettes = {}
        if not os.path.exists(self.themes_dir):
            os.makedirs(self.themes_dir, exist_ok=True)
            
        for item in os.listdir(self.themes_dir):
            item_path = os.path.join(self.themes_dir, item)
            if os.path.isdir(item_path):
                json_path = os.path.join(item_path, "theme.json")
                if os.path.exists(json_path):
                    try:
                        with open(json_path, "r", encoding="utf-8") as f:
                            self.palettes[item] = json.load(f)
                    except Exception as e:
                        print(f"[ThemeManager] Lỗi nạp theme {item}: {e}")
                        
        if "classic" not in self.palettes:
            self.palettes["classic"] = self._get_fallback_classic_palette()

    def get_available_themes(self) -> list:
        return list(self.palettes.keys())

    def get_current_theme(self) -> str:
        return self._current_theme

    def get_color(self, color_name: str) -> str:
        theme_palettes = self.palettes.get(self._current_theme, self.palettes.get("classic"))
        mode = self.mode_manager.get_current_mode()
        mode_palette = theme_palettes.get(mode, theme_palettes.get("dark", {}))
        
        if color_name not in mode_palette:
            classic_palette = self.palettes.get("classic", {}).get(mode, {})
            return classic_palette.get(color_name, "#ffffff")
        return mode_palette.get(color_name, "#ffffff")

    def switch_theme(self, theme_name: str):
        if theme_name not in self.palettes:
            return
        self._current_theme = theme_name
        self._notify_changes()

    def _handle_mode_change(self, mode: str):
        self._notify_changes()

    def _notify_changes(self):
        qss = self.get_formatted_qss()
        for callback in self._listeners:
            try:
                callback(self._current_theme, qss)
            except Exception as e:
                print(f"[ThemeManager] Lỗi gọi callback: {e}")

    def get_formatted_qss(self) -> str:
        theme_palettes = self.palettes.get(self._current_theme, self.palettes.get("classic"))
        mode = self.mode_manager.get_current_mode()
        palette = theme_palettes.get(mode, theme_palettes.get("dark", {}))
        
        classic_palette = self.palettes.get("classic", {}).get(mode, self.palettes.get("classic", {}).get("dark", {}))
        final_palette = {**classic_palette, **palette}
        
        qss_content = ""
        if os.path.exists(self.qss_path):
            try:
                with open(self.qss_path, "r", encoding="utf-8") as f:
                    qss_content = f.read()
            except Exception as e:
                print(f"[ThemeManager] Lỗi đọc base QSS: {e}")
                
        qss = qss_content
        for key, val in final_palette.items():
            qss = qss.replace(f"{{{key}}}", str(val))
            
        custom_qss_path = os.path.join(self.themes_dir, self._current_theme, "theme.qss")
        if os.path.exists(custom_qss_path):
            try:
                with open(custom_qss_path, "r", encoding="utf-8") as f:
                    custom_qss = f.read()
                    for key, val in final_palette.items():
                        custom_qss = custom_qss.replace(f"{{{key}}}", str(val))
                    qss += "\\n" + custom_qss
            except Exception as e:
                print(f"[ThemeManager] Lỗi nạp custom QSS: {e}")
                
        return qss

    def _get_fallback_classic_palette(self) -> dict:
        return {
            "dark": {
                "DARK_BG": "#1e1e2e",
                "SIDEBAR_BG": "#11111b",
                "CARD_BG": "#181825",
                "TEXT_COLOR": "#cdd6f4",
                "SUBTEXT_COLOR": "#a6adc8",
                "ACCENT_COLOR": "#89b4fa",
                "ACCENT_HOVER": "#b4befe",
                "SUCCESS_COLOR": "#a6e3a1",
                "ERROR_COLOR": "#f38ba8",
                "BORDER_COLOR": "#313244",
                "RADIUS": "8px",
                "BORDER_WIDTH": "1px",
                "FONT_FAMILY": "Inter, Roboto, sans-serif"
            },
            "light": {
                "DARK_BG": "#f8f9fa",
                "SIDEBAR_BG": "#e9ecef",
                "CARD_BG": "#ffffff",
                "TEXT_COLOR": "#212529",
                "SUBTEXT_COLOR": "#6c757d",
                "ACCENT_COLOR": "#4f46e5",
                "ACCENT_HOVER": "#4338ca",
                "SUCCESS_COLOR": "#10b981",
                "ERROR_COLOR": "#ef4444",
                "BORDER_COLOR": "#dee2e6",
                "RADIUS": "8px",
                "BORDER_WIDTH": "1px",
                "FONT_FAMILY": "Inter, Roboto, sans-serif"
            }
        }
'''

BASE_QSS_TEMPLATE = """/* Main Application Window & Containers */
QMainWindow {
    background-color: {DARK_BG};
}
QWidget {
    font-family: {FONT_FAMILY};
    color: {TEXT_COLOR};
}

/* Sidebar Styling */
QFrame#sidebar {
    background-color: {SIDEBAR_BG};
    border-right: {BORDER_WIDTH} solid {BORDER_COLOR};
}

/* Content Container Styling */
QWidget#content_container {
    background-color: {DARK_BG};
}

/* Stat Cards / Group Box Styling */
QFrame {
    background-color: {CARD_BG};
    border: {BORDER_WIDTH} solid {BORDER_COLOR};
    border-radius: {RADIUS};
}

/* Line Edits / Text Areas */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: {DARK_BG};
    color: {TEXT_COLOR};
    border: {BORDER_WIDTH} solid {BORDER_COLOR};
    border-radius: {RADIUS};
    padding: 10px;
}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: {BORDER_WIDTH} solid {ACCENT_COLOR};
}

/* --- Atom Buttons --- */
QPushButton[class="PrimaryButton"] {
    background-color: {ACCENT_COLOR};
    color: {SIDEBAR_BG};
    font-size: 14px;
    font-weight: bold;
    padding: 10px 20px;
    border-radius: {RADIUS};
    border: none;
}
QPushButton[class="PrimaryButton"]:hover {
    background-color: {ACCENT_HOVER};
}

QPushButton[class="NavButton"] {
    color: {TEXT_COLOR};
    background-color: transparent;
    border: none;
    border-left: 4px solid transparent;
    text-align: left;
    padding: 12px 15px;
    font-size: 13px;
    border-radius: 0px;
}
QPushButton[class="NavButton"]:hover {
    background-color: {CARD_BG};
    color: {ACCENT_COLOR};
}
QPushButton[class="NavButton"]:checked {
    background-color: {CARD_BG};
    color: {ACCENT_COLOR};
    border-left: 4px solid {ACCENT_COLOR};
    font-weight: bold;
}

QPushButton[class="SecondaryButton"] {
    background-color: transparent;
    color: {ACCENT_COLOR};
    border: 2px solid {ACCENT_COLOR};
    border-radius: {RADIUS};
    padding: 10px 20px;
    font-weight: bold;
    font-size: 13px;
}
QPushButton[class="SecondaryButton"]:hover {
    background-color: {ACCENT_COLOR};
    color: {SIDEBAR_BG};
}

/* --- Atom Inputs & Labels --- */
QLineEdit[class="FormLineEdit"] {
    background-color: {DARK_BG};
    color: {TEXT_COLOR};
    border: {BORDER_WIDTH} solid {BORDER_COLOR};
    border-radius: {RADIUS};
    padding: 8px 12px;
    font-size: 13px;
}
QLineEdit[class="FormLineEdit"]:focus {
    border: {BORDER_WIDTH} solid {ACCENT_COLOR};
}

QLabel[class="HeaderLabel"] {
    font-size: 20px;
    font-weight: bold;
    color: {TEXT_COLOR};
}
QLabel[class="SubtitleLabel"] {
    font-size: 15px;
    font-weight: bold;
    color: {TEXT_COLOR};
}
QLabel[class="BodyLabel"] {
    font-size: 13px;
    color: {SUBTEXT_COLOR};
}

/* --- Settings Container & Combo --- */
QComboBox {
    background-color: {SIDEBAR_BG};
    border: {BORDER_WIDTH} solid {BORDER_COLOR};
    color: {TEXT_COLOR};
    padding: 4px 6px;
    font-size: 11px;
    border-radius: 4px;
}
QComboBox QAbstractItemView {
    background-color: {SIDEBAR_BG};
    color: {TEXT_COLOR};
    selection-background-color: {ACCENT_COLOR};
    selection-color: {SIDEBAR_BG};
    border: {BORDER_WIDTH} solid {BORDER_COLOR};
}
QFrame#settings_container {
    background-color: {CARD_BG};
    border: {BORDER_WIDTH} solid {BORDER_COLOR};
    border-radius: {RADIUS};
    padding: 6px;
}
"""

CLASSIC_THEME_JSON_TEMPLATE = """{
    "dark": {
        "DARK_BG": "#1e1e2e",
        "SIDEBAR_BG": "#11111b",
        "CARD_BG": "#181825",
        "TEXT_COLOR": "#cdd6f4",
        "SUBTEXT_COLOR": "#a6adc8",
        "ACCENT_COLOR": "#89b4fa",
        "ACCENT_HOVER": "#b4befe",
        "SUCCESS_COLOR": "#a6e3a1",
        "ERROR_COLOR": "#f38ba8",
        "BORDER_COLOR": "#313244",
        "RADIUS": "8px",
        "BORDER_WIDTH": "1px",
        "FONT_FAMILY": "Inter, Roboto, sans-serif"
    },
    "light": {
        "DARK_BG": "#f8f9fa",
        "SIDEBAR_BG": "#e9ecef",
        "CARD_BG": "#ffffff",
        "TEXT_COLOR": "#212529",
        "SUBTEXT_COLOR": "#6c757d",
        "ACCENT_COLOR": "#4f46e5",
        "ACCENT_HOVER": "#4338ca",
        "SUCCESS_COLOR": "#10b981",
        "ERROR_COLOR": "#ef4444",
        "BORDER_COLOR": "#dee2e6",
        "RADIUS": "8px",
        "BORDER_WIDTH": "1px",
        "FONT_FAMILY": "Inter, Roboto, sans-serif"
    }
}"""

CLASSIC_THEME_QSS_TEMPLATE = """/* Classic Theme Custom Stylesheet Override */
"""

BASE_PAGE_TEMPLATE = '''from PyQt6.QtWidgets import QWidget, QVBoxLayout
from ..level_01_atoms.labels import HeaderLabel

class BasePageTemplate(QWidget):
    """
    Template cấp độ 4 (Templates) trong thiết kế Atomic UI.
    Định nghĩa cấu trúc layout chung cho tất cả các trang con.
    """
    def __init__(self, title_key: str, app_ctx, parent=None):
        super().__init__(parent)
        self.app_ctx = app_ctx
        self.theme_manager = app_ctx.theme_manager
        self.i18n_manager = app_ctx.i18n_manager
        self.title_key = title_key
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)
        
        self.header = HeaderLabel(self.i18n_manager.translate(self.title_key))
        self.main_layout.addWidget(self.header)
        
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(15)
        self.main_layout.addWidget(self.content_widget, stretch=1)
        
        self.i18n_manager.subscribe(self._handle_language_changed)

    def _handle_language_changed(self, lang_code: str):
        self.header.setText(self.i18n_manager.translate(self.title_key))
        self.retranslate_ui(lang_code)

    def retranslate_ui(self, lang_code: str):
        pass
'''

EN_JSON_TEMPLATE = """{
    "LanguageName": "English",
    "settings": "Settings",
    "theme": "Theme",
    "language": "Language",
    "mode": "Mode"
}"""

VI_JSON_TEMPLATE = """{
    "LanguageName": "Tiếng Việt",
    "settings": "Cấu hình",
    "theme": "Chủ đề",
    "language": "Ngôn ngữ",
    "mode": "Chế độ"
}"""

ZH_JSON_TEMPLATE = """{
    "LanguageName": "简体中文",
    "settings": "设置",
    "theme": "主题",
    "language": "语言",
    "mode": "模式"
}"""
