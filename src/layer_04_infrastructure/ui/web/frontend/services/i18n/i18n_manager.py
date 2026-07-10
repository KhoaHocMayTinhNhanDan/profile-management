import os
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
