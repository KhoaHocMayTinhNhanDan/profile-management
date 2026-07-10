class LightDarkModeManager:
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
