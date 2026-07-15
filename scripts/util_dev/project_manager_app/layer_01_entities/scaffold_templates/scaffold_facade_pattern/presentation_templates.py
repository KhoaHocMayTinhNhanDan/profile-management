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

    [Cơ chế Mở rộng Theme]:
    Hệ thống hỗ trợ cơ chế cắm-rút 100%. Để thêm một theme mới (ví dụ: 'cyberpunk'), bạn chỉ cần:
    1. Tạo một thư mục mới tại 'themes/cyberpunk/'
    2. Đặt vào đó tệp 'theme.json' định nghĩa bảng màu và 'theme.qss' định nghĩa CSS ghi đè.
    Hệ thống sẽ tự động quét, hiển thị trên giao diện và áp dụng khi người dùng lựa chọn.
    Chi tiết hướng dẫn tại tệp 'themes/README.md'.
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
                palette_json = os.path.join(item_path, "07_color_palettes", "theme.json")
                if os.path.exists(palette_json):
                    try:
                        combined_data = {}
                        with open(palette_json, "r", encoding="utf-8") as f:
                            palette_data = json.load(f)
                        
                        modes = ["dark", "light"]
                        for mode in modes:
                            if mode in palette_data:
                                combined_data[mode] = {**palette_data[mode]}
                            else:
                                combined_data[mode] = {}
                        
                        pillars = ["01_geometry_borders", "02_typography", "03_spacing", "04_shadows_elevation", "05_motion_animations"]
                        for sub in pillars:
                            p_json = os.path.join(item_path, sub, "theme.json")
                            if os.path.exists(p_json):
                                try:
                                    with open(p_json, "r", encoding="utf-8") as f:
                                        p_data = json.load(f)
                                    for mode in modes:
                                        combined_data[mode].update(p_data)
                                except Exception:
                                    pass
                        self.palettes[item] = combined_data
                    except Exception as e:
                        print(f"[ThemeManager] Lỗi nạp theme {item}: {e}")
                        
        if "classic" not in self.palettes:
            self.palettes["classic"] = self._get_fallback_classic_palette()

    def get_available_themes(self) -> list:
        return list(self.palettes.keys())

    def get_current_theme(self) -> str:
        return self._current_theme

    def get_color(self, color_name: str) -> str:
        theme_palettes = self.palettes.get(self._current_theme) or self.palettes.get("classic") or {}
        mode = self.mode_manager.get_current_mode()
        mode_palette = theme_palettes.get(mode) or theme_palettes.get("dark") or {}
        
        if color_name not in mode_palette:
            classic_palette = (self.palettes.get("classic") or {}).get(mode) or {}
            return classic_palette.get(color_name, "#ffffff")
        return mode_palette.get(color_name, "#ffffff")

    def get_token(self, token_name: str) -> str:
        """
        Lấy giá trị của một Design Token động (màu sắc, hình học, font, spacing...).
        """
        return self.get_color(token_name)

    def get_asset_path(self, asset_name: str) -> str:
        """
        Lấy đường dẫn tuyệt đối động của file tài nguyên (asset) đi kèm theme.
        Tự động fallback về theme classic nếu theme hiện tại thiếu file.
        """
        ext = os.path.splitext(asset_name)[1].lower()
        sub_folder = "icons"
        if ext in [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"]:
            sub_folder = "images" if ext != ".svg" else "icons"
        elif ext in [".ttf", ".otf", ".woff", ".woff2"]:
            sub_folder = "fonts"
            
        path = os.path.join(self.themes_dir, self._current_theme, "06_visual_assets", sub_folder, asset_name)
        if os.path.exists(path):
            return path.replace("\\\\", "/")
            
        path_flat = os.path.join(self.themes_dir, self._current_theme, "06_visual_assets", asset_name)
        if os.path.exists(path_flat):
            return path_flat.replace("\\\\", "/")
            
        path_classic = os.path.join(self.themes_dir, "classic", "06_visual_assets", sub_folder, asset_name)
        if os.path.exists(path_classic):
            return path_classic.replace("\\\\", "/")
            
        return os.path.join(self.themes_dir, "classic", "06_visual_assets", asset_name).replace("\\\\", "/")

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
        theme_palettes = self.palettes.get(self._current_theme) or self.palettes.get("classic") or {}
        mode = self.mode_manager.get_current_mode()
        palette = theme_palettes.get(mode) or theme_palettes.get("dark") or {}
        
        classic_palette = (self.palettes.get("classic") or {}).get(mode) or (self.palettes.get("classic") or {}).get("dark") or {}
        final_palette = {**classic_palette, **palette}
        
        qss_content = ""
        if os.path.exists(self.qss_path):
            try:
                with open(self.qss_path, "r", encoding="utf-8") as f:
                    qss_content = f.read() + "\\n"
            except Exception as e:
                print(f"[ThemeManager] Lỗi đọc base QSS: {e}")
                
        # Quét đệ quy tìm toàn bộ các file .qss ở level_01 đến level_04
        ui_root = os.path.dirname(os.path.dirname(self.base_dir))
        levels = ["level_01_atoms", "level_02_molecules", "level_03_organisms", "level_04_templates"]
        for lvl in levels:
            lvl_path = os.path.join(ui_root, lvl)
            if os.path.exists(lvl_path):
                for root_dir, _, files in os.walk(lvl_path):
                    for file in files:
                        if file.endswith(".qss"):
                            file_path = os.path.join(root_dir, file)
                            try:
                                with open(file_path, "r", encoding="utf-8") as f:
                                    qss_content += f.read() + "\\n"
                            except Exception as e:
                                print(f"[ThemeManager] Lỗi nạp QSS từ {file_path}: {e}")
                                
        # Tự động quét toàn bộ assets tĩnh trong theme mặc định (classic) để tạo Fallback Base
        classic_assets_dir = os.path.join(self.themes_dir, "classic", "06_visual_assets")
        if os.path.exists(classic_assets_dir):
            for root_dir, _, files in os.walk(classic_assets_dir):
                for file_name in files:
                    file_path = os.path.join(root_dir, file_name)
                    base_name, _ = os.path.splitext(file_name)
                    key = f"THEME_ASSET_{base_name.upper()}"
                    final_palette[key] = file_path.replace("\\\\", "/")

        # Quét và ghi đè bằng assets của theme hiện tại
        current_assets_dir = os.path.join(self.themes_dir, self._current_theme, "06_visual_assets")
        if os.path.exists(current_assets_dir) and self._current_theme != "classic":
            for root_dir, _, files in os.walk(current_assets_dir):
                for file_name in files:
                    file_path = os.path.join(root_dir, file_name)
                    base_name, _ = os.path.splitext(file_name)
                    key = f"THEME_ASSET_{base_name.upper()}"
                    final_palette[key] = file_path.replace("\\\\", "/")

        # Khai báo fallback tương thích ngược cho biến cũ
        if "THEME_ASSET_DOWN_ARROW" in final_palette:
            final_palette["DOWN_ARROW_URL"] = final_palette["THEME_ASSET_DOWN_ARROW"]
        
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
    padding: {INPUT_PADDING};
}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: {BORDER_WIDTH} solid {ACCENT_COLOR};
}

/* --- Settings Container & Combo --- */
QComboBox {
    background-color: {SIDEBAR_BG};
    border: {BORDER_WIDTH} solid {BORDER_COLOR};
    color: {TEXT_COLOR};
    padding: {COMBO_PADDING};
    font-size: {INPUT_FONT_SIZE};
    border-radius: {RADIUS};
}
QComboBox QAbstractItemView {
    background-color: {SIDEBAR_BG};
    color: {TEXT_COLOR};
    selection-background-color: {ACCENT_COLOR};
    selection-color: {SIDEBAR_BG};
    border: {BORDER_WIDTH} solid {BORDER_COLOR};
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 20px;
    border-left: {BORDER_WIDTH} solid {BORDER_COLOR};
    border-top-right-radius: {RADIUS};
    border-bottom-right-radius: {RADIUS};
    background-color: {DARK_BG};
}
QComboBox::down-arrow {
    image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMiIgaGVpZ2h0PSIxMiIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNjZGQ2ZjQiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cG9seWxpbmUgcG9pbnRzPSI2IDkgMTIgMTUgMTggOSI+PC9wb2x5bGluZT48L3N2Zz4=");
    width: 10px;
    height: 10px;
}
QFrame#settings_container {
    background-color: {CARD_BG};
    border: {BORDER_WIDTH} solid {BORDER_COLOR};
    border-radius: {RADIUS};
    padding: {SPACING_BASE};
}

/* Dialogs & Message Boxes */
QDialog, QMessageBox {
    background-color: {CARD_BG};
    color: {TEXT_COLOR};
}
QMessageBox QLabel {
    color: {TEXT_COLOR};
    background-color: transparent;
}
QMessageBox QPushButton {
    background-color: {ACCENT_COLOR};
    color: {SIDEBAR_BG};
    border: {BORDER_WIDTH} solid {ACCENT_COLOR};
    border-radius: {RADIUS};
    padding: {BUTTON_PADDING};
    font-weight: bold;
}
QMessageBox QPushButton:hover {
    background-color: {ACCENT_HOVER};
    border-color: {ACCENT_HOVER};
}
"""

CLASSIC_THEME_JSON_TEMPLATE = """{{
    "dark": {{
        "DARK_BG": "#1e1e2e",
        "SIDEBAR_BG": "#11111b",
        "CARD_BG": "#181825",
        "TEXT_COLOR": "#cdd6f4",
        "SUBTEXT_COLOR": "#a6adc8",
        "ACCENT_COLOR": "{ACCENT_COLOR_DARK}",
        "ACCENT_HOVER": "{ACCENT_HOVER_DARK}",
        "SUCCESS_COLOR": "#a6e3a1",
        "ERROR_COLOR": "#f38ba8",
        "BORDER_COLOR": "#313244",
        "RADIUS": "8px",
        "BORDER_WIDTH": "1px",
        "FONT_FAMILY": "{FONT_FAMILY}"
    }},
    "light": {{
        "DARK_BG": "#f8f9fa",
        "SIDEBAR_BG": "#e9ecef",
        "CARD_BG": "#ffffff",
        "TEXT_COLOR": "#212529",
        "SUBTEXT_COLOR": "#6c757d",
        "ACCENT_COLOR": "{ACCENT_COLOR_LIGHT}",
        "ACCENT_HOVER": "{ACCENT_HOVER_LIGHT}",
        "SUCCESS_COLOR": "#10b981",
        "ERROR_COLOR": "#ef4444",
        "BORDER_COLOR": "#dee2e6",
        "RADIUS": "8px",
        "BORDER_WIDTH": "1px",
        "FONT_FAMILY": "{FONT_FAMILY}"
    }}
}}"""

CLASSIC_THEME_QSS_TEMPLATE = """/* Classic Theme Custom Stylesheet Override */
"""

BASE_PAGE_TEMPLATE = '''from PyQt6.QtWidgets import QWidget, QVBoxLayout
from ...level_01_atoms import HeaderLabel

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

SETTINGS_STORE_TEMPLATE = '''import os
import json

class SettingsStore:
    """
    SettingsStore - Quản lý đọc/ghi cấu hình giao diện người dùng cục bộ tự động.
    Lưu trữ cấu hình trong tệp settings.json tại thư mục cha của services/ (tức root ui).
    """
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.config_path = os.path.join(self.base_dir, "settings.json")
        self.settings = {
            "theme": "classic",
            "mode": "dark",
            "language": "en"
        }
        self.load()

    def load(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        self.settings.update(data)
            except Exception as e:
                print(f"[SettingsStore] Lỗi đọc cấu hình: {e}")

    def save(self):
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4)
        except Exception as e:
            print(f"[SettingsStore] Lỗi ghi cấu hình: {e}")

    def get(self, key: str, default: str) -> str:
        val = self.settings.get(key, default)
        return str(val) if val is not None else default

    def set(self, key: str, value):
        if self.settings.get(key) != value:
            self.settings[key] = value
            self.save()
'''

THEMES_README_TEMPLATE = """# 🎨 Hướng dẫn Tùy biến & Mở rộng Theme Giao diện (Plug-and-Play Theme System)

Dự án này tích hợp sẵn một hệ thống quản lý Theme động cực kỳ linh hoạt và mạnh mẽ dựa trên triết lý **W3C Design Tokens**. Để đảm bảo tính tổng quát và sạch sẽ, dự án mặc định chỉ chứa Theme `classic`.

Nếu bạn muốn mở rộng hoặc thêm các Theme mới (ví dụ: `cyberpunk`, `space_dark`...), bạn chỉ cần làm theo hướng dẫn dưới đây mà không cần sửa bất kỳ dòng code Python nào của bộ máy quản lý (`ThemeManager`).

---

## 🚀 Các bước thêm một Theme mới

### Bước 1: Tạo thư mục Theme mới
Tạo một thư mục con nằm trong thư mục này (`src/layer_04_infrastructure/ui/desktop_qt6/services/theme/themes/`) đặt tên theo theme của bạn (chữ thường, viết liền hoặc snake_case).
*Ví dụ: Tạo thư mục `cyberpunk/`*

### Bước 2: Tạo cấu trúc 7 Trụ cột (W3C Design Tokens)
Bên trong thư mục theme vừa tạo, thiết lập cấu trúc các thư mục con sau:
```text
cyberpunk/
├── 01_geometry_borders/     <-- Radius, Border Width
│   └── theme.json
├── 02_typography/           <-- Fonts, Font Sizes (Header, Body, Console)
│   └── theme.json
├── 03_spacing/              <-- Paddings, Spacing, Heights
│   └── theme.json
├── 04_shadows_elevation/    <-- Elevations, Shadows
│   └── theme.json
├── 05_motion_animations/    <-- Animation transitions
│   └── theme.json
├── 06_visual_assets/        <-- Subfolders: images/, fonts/, icons/
└── 07_color_palettes/       <-- Color palettes (dark & light modes)
    └── theme.json
```

#### Định nghĩa ví dụ các tệp tin `theme.json`:

*   **`07_color_palettes/theme.json` (Bắt buộc phải có - định nghĩa màu sắc cho dark/light modes):**
    ```json
    {
        "dark": {
            "DARK_BG": "#0a051b",
            "SIDEBAR_BG": "#120b2e",
            "CARD_BG": "#1f1445",
            "TEXT_COLOR": "#00ffcc",
            "SUBTEXT_COLOR": "#ff007f",
            "ACCENT_COLOR": "#ff007f",
            "ACCENT_HOVER": "#00ffcc",
            "SUCCESS_COLOR": "#00ff66",
            "ERROR_COLOR": "#ff3333",
            "BORDER_COLOR": "#00ffcc"
        },
        "light": {
            "DARK_BG": "#faf5ff",
            "SIDEBAR_BG": "#f3e8ff",
            "CARD_BG": "#ffffff",
            "TEXT_COLOR": "#581c87",
            "SUBTEXT_COLOR": "#701a75",
            "ACCENT_COLOR": "#a21caf",
            "ACCENT_HOVER": "#86198f",
            "SUCCESS_COLOR": "#16a34a",
            "ERROR_COLOR": "#dc2626",
            "BORDER_COLOR": "#d8b4fe"
        }
    }
    ```

*   **`01_geometry_borders/theme.json`:**
    ```json
    {
        "RADIUS": "0px",
        "RADIUS_NUM": "0",
        "BORDER_WIDTH": "2px",
        "CHECKBOX_RADIUS": "0px",
        "PROGRESS_RADIUS": "0px",
        "CONSOLE_RADIUS": "0px"
    }
    ```

*   **`02_typography/theme.json`:**
    ```json
    {
        "FONT_FAMILY": "Courier New, monospace",
        "BUTTON_FONT_SIZE": "12px",
        "INPUT_FONT_SIZE": "12px",
        "HEADER_FONT_SIZE": "14px",
        "BODY_FONT_SIZE": "10px",
        "CONSOLE_FONT_SIZE": "11px",
        "STATUS_FONT_SIZE": "10px"
    }
    ```

*   **`03_spacing/theme.json`:**
    ```json
    {
        "SPACING_BASE": "4px",
        "BUTTON_PADDING": "8px 16px",
        "INPUT_PADDING": "6px 10px",
        "LABEL_MARGIN_BOTTOM": "8px",
        "COMBO_PADDING": "4px 28px 4px 8px",
        "CARD_PADDING": "10px",
        "CHECKBOX_SPACING": "6px",
        "CONSOLE_PADDING": "8px",
        "PROGRESS_HEIGHT": "18px"
    }
    ```

### Bước 3 (Tùy chọn): Tạo tệp `theme.qss` ghi đè
Nếu bạn muốn bổ sung CSS/QSS tùy biến dành riêng cho Theme này (ví dụ: tạo hiệu ứng viền neon, hiệu ứng đổ bóng đặc biệt), hãy tạo tệp `theme.qss` ở thư mục gốc của theme đó.
*Ví dụ: `themes/cyberpunk/theme.qss`*
```css
/* Tự động nạp và ghi đè kiểu dáng cho riêng theme Cyberpunk */
QPushButton {
    border: {BORDER_WIDTH} solid {ACCENT_COLOR};
    border-radius: {RADIUS};
}
```

---

## 🛠️ Cách hoạt động của ThemeManager

1. **Tự động quét (Autoloading)**: Khi khởi chạy ứng dụng, `ThemeManager` sẽ quét thư mục `themes/` tìm tệp `07_color_palettes/theme.json` để đăng ký theme (tên thư mục sẽ làm ID theme, ví dụ: `"cyberpunk"`). Sau đó, nó tự động quét và nạp chồng các thông số hình học/khoảng cách/typography từ các folder `01_...` đến `05_...` tương ứng nếu có.
2. **Dynamic UI Rendering**: Toàn bộ QSS trong các component Atoms/Molecules viết dưới dạng các biến placeholder (ví dụ: `{ACCENT_COLOR}`, `{RADIUS}`) sẽ tự động được biên dịch sang giá trị tương ứng của theme đang chọn.
3. **Cập nhật tức thì (Reactive)**: Khi người dùng đổi theme hoặc chuyển chế độ sáng/tối, tín hiệu thay đổi được phát đi và toàn bộ giao diện sẽ chuyển đổi trạng thái màu sắc ngay lập tức mà không cần khởi động lại ứng dụng.
"""

ASSETS_LOADER_TEMPLATE = '''import os
import inspect
from PyQt6.QtCore import QByteArray, Qt
from PyQt6.QtGui import QIcon, QPixmap, QPainter
from PyQt6.QtSvg import QSvgRenderer

class AssetsLoader:
    """
    AssetsLoader - Hỗ trợ nạp tài nguyên cục bộ đi kèm (colocated assets) cho các Component.
    Hỗ trợ tìm và trả về đường dẫn tuyệt đối cho icon/hình ảnh và nạp trực tiếp QIcon.
    """
    _icon_cache = {}

    @classmethod
    def load_theme_icon(cls, relative_path: str, color_hex: str | None = None) -> QIcon:
        """
        Nạp icon SVG cục bộ, tự động đổi màu theo màu sắc truyền vào và lưu vào Cache.
        Tự động phân giải thư mục của file gọi thông qua inspect stack.
        """
        # Tự động xác định thư mục của Component gọi hàm này (ở stack level 1)
        try:
            caller_frame = inspect.stack()[1]
            caller_dir = os.path.dirname(os.path.abspath(caller_frame.filename))
            abs_path = os.path.normpath(os.path.join(caller_dir, relative_path))
        except Exception:
            return QIcon()

        if not os.path.exists(abs_path):
            return QIcon()

        # Nếu không yêu cầu đổi màu hoặc không phải SVG, nạp QIcon chuẩn và đưa vào cache
        if not color_hex or not abs_path.endswith(".svg"):
            cache_key = (abs_path, "original")
            if cache_key in cls._icon_cache:
                return cls._icon_cache[cache_key]
            icon = QIcon(abs_path)
            cls._icon_cache[cache_key] = icon
            return icon

        # Nếu đổi màu SVG: Kiểm tra trong Cache trước
        cache_key = (abs_path, color_hex)
        if cache_key in cls._icon_cache:
            return cls._icon_cache[cache_key]

        # Đọc nội dung SVG và đổi màu trực tiếp trong bộ nhớ RAM
        try:
            with open(abs_path, "r", encoding="utf-8") as f:
                svg_content = f.read()

            # Thay thế các màu mặc định trong file SVG sang màu sắc của Theme mới
            recolored_svg = svg_content.replace('currentColor', color_hex)
            recolored_svg = recolored_svg.replace('#000000', color_hex)
            recolored_svg = recolored_svg.replace('#333333', color_hex)

            # Biến chuỗi XML đã đổi màu thành QByteArray
            byte_array = QByteArray(recolored_svg.encode("utf-8"))
            renderer = QSvgRenderer(byte_array)

            # Vẽ SVG đã đổi màu lên một QPixmap trong suốt
            pixmap = QPixmap(24, 24)  # Kích thước icon chuẩn
            pixmap.fill(Qt.GlobalColor.transparent)
            
            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.end()

            # Tạo QIcon từ pixmap vừa vẽ và đưa vào bộ nhớ đệm
            icon = QIcon(pixmap)
            cls._icon_cache[cache_key] = icon
            return icon
        except Exception:
            # Fallback: Trả về icon nguyên bản nếu có lỗi xảy ra
            return QIcon(abs_path)

    @staticmethod
    def load_qss(caller_file: str, relative_path: str) -> str:
        """
        Đọc nội dung file QSS cục bộ đi kèm của component.
        """
        path = os.path.abspath(os.path.normpath(os.path.join(os.path.dirname(caller_file), relative_path)))
        if not os.path.exists(path):
            return ""
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def get_path(caller_file: str, *path_segments: str) -> str:
        """
        Phân giải đường dẫn tuyệt đối động của tài nguyên dựa vào tệp gọi caller_file (__file__).
        """
        return os.path.abspath(os.path.join(os.path.dirname(caller_file), *path_segments))
'''
