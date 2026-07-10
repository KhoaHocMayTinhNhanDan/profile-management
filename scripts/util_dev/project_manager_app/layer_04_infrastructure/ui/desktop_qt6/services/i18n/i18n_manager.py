import os
import json
from PyQt6.QtCore import QObject, pyqtSignal

class I18nManager(QObject):
    """
    Dịch vụ quản lý Đa ngôn ngữ (i18n) động.
    Tải từ điển dịch thuật từ các file JSON tương ứng trong thư mục /locales/ khi đổi ngôn ngữ.
    """
    language_changed = pyqtSignal(str)

    def __init__(self, current_lang: str = "en"):
        super().__init__()
        self._current_lang = current_lang
        self._dictionary = {}
        self._load_translations(current_lang)

    def get_current_lang(self) -> str:
        return self._current_lang

    def get_available_languages(self) -> dict:
        """
        Quét thư mục locales/ và trả về dict của {lang_code: language_name}
        """
        langs = {}
        locales_dir = os.path.join(os.path.dirname(__file__), "locales")
        if os.path.exists(locales_dir):
            for file in os.listdir(locales_dir):
                if file.endswith(".json"):
                    lang_code = file[:-5]
                    # Đọc tạm để lấy LanguageName
                    json_path = os.path.join(locales_dir, file)
                    try:
                        with open(json_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            langs[lang_code] = data.get("LanguageName", lang_code)
                    except Exception:
                        langs[lang_code] = lang_code
        # Sắp xếp English lên đầu, sau đó đến các ngôn ngữ khác
        sorted_langs = {}
        if "en" in langs:
            sorted_langs["en"] = langs["en"]
        for code, name in sorted(langs.items()):
            if code != "en":
                sorted_langs[code] = name
        return sorted_langs

    def _load_translations(self, lang_code: str):
        self._dictionary = {}
        # Tìm đường dẫn đến thư mục chứa các file json locales
        locales_dir = os.path.join(os.path.dirname(__file__), "locales")
        json_path = os.path.join(locales_dir, f"{lang_code}.json")
        
        if os.path.exists(json_path):
            try:
                with open(json_path, "r", encoding="utf-8") as f:
                    self._dictionary = json.load(f)
            except Exception as e:
                print(f"Lỗi khi đọc file ngôn ngữ {lang_code}: {e}")

    def switch_language(self, lang_code: str):
        self._current_lang = lang_code
        self._load_translations(lang_code)
        self.language_changed.emit(lang_code)

    def translate(self, text: str, **kwargs) -> str:
        # Lấy từ bản dịch, nếu không có thì trả về chính key làm fallback
        translated = self._dictionary.get(text, text)
        if kwargs:
            try:
                return translated.format(**kwargs)
            except Exception:
                pass
        return translated
