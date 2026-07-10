import os
import json
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication

class ThemeManager(QObject):
    """
    ThemeManager - Dịch vụ quản lý Theme cắm-rút động (Plug-and-Play).
    Tự động quét cấu hình từ thư mục `themes/` và nạp stylesheet từ `base.qss`.
    """
    theme_changed = pyqtSignal(str)

    def __init__(self, mode_manager, default_theme: str = "classic"):
        super().__init__()
        self.mode_manager = mode_manager
        
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.themes_dir = os.path.join(self.base_dir, "themes")
        self.qss_path = os.path.join(self.base_dir, "base.qss")
        
        self.palettes = {}
        self.load_available_themes()
        
        self._current_theme = default_theme if default_theme in self.palettes else "classic"
        self.mode_manager.mode_changed.connect(self._handle_mode_change)

    def load_available_themes(self):
        """Quét các thư mục con trong themes/ để nạp động cấu hình theme.json."""
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
                        print(f"[ThemeManager] Error loading theme {item}: {e}")
                        
        # Đảm bảo luôn có classic theme làm dự phòng tối thiểu
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
        
        # Fallback cơ chế: nếu thiếu từ khóa, tìm trong classic theme
        if color_name not in mode_palette:
            classic_palette = self.palettes.get("classic", {}).get(mode, {})
            return classic_palette.get(color_name, "#ffffff")
        return mode_palette.get(color_name, "#ffffff")

    def switch_theme(self, theme_name: str):
        if theme_name not in self.palettes:
            return
        self._current_theme = theme_name
        self.apply_theme_to_app()
        self.theme_changed.emit(theme_name)

    def _handle_mode_change(self, mode: str):
        self.apply_theme_to_app()
        self.theme_changed.emit(self._current_theme)

    def apply_theme_to_app(self):
        app = QApplication.instance()
        if not app:
            return
            
        theme_palettes = self.palettes.get(self._current_theme, self.palettes.get("classic"))
        mode = self.mode_manager.get_current_mode()
        palette = theme_palettes.get(mode, theme_palettes.get("dark", {}))
        
        # Merge với classic palette làm fallback nếu thiếu keys để tránh KeyError khi format QSS
        classic_palette = self.palettes.get("classic", {}).get(mode, self.palettes.get("classic", {}).get("dark", {}))
        final_palette = {**classic_palette, **palette}
        
        # Đọc QSS base
        qss_content = ""
        if os.path.exists(self.qss_path):
            try:
                with open(self.qss_path, "r", encoding="utf-8") as f:
                    qss_content = f.read()
            except Exception as e:
                print(f"[ThemeManager] Error reading base QSS: {e}")
                
        # Nạp và thay thế các từ khóa trong QSS với palette
        qss = qss_content
        for key, val in final_palette.items():
            qss = qss.replace(f"{{{key}}}", str(val))
            
        # Nạp thêm QSS tùy chọn đặc thù của theme (nếu có tệp custom)
        custom_qss_path = os.path.join(self.themes_dir, self._current_theme, "theme.qss")
        if os.path.exists(custom_qss_path):
            try:
                with open(custom_qss_path, "r", encoding="utf-8") as f:
                    custom_qss = f.read()
                    for key, val in final_palette.items():
                        custom_qss = custom_qss.replace(f"{{{key}}}", str(val))
                    qss += "\n" + custom_qss
            except Exception as e:
                print(f"[ThemeManager] Error loading custom QSS for theme {self._current_theme}: {e}")
                
        app.setStyleSheet(qss)

    def _get_fallback_classic_palette(self) -> dict:
        """Bộ màu dự phòng tối thiểu nếu thiếu tệp JSON cấu hình."""
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
