from PyQt6.QtCore import QObject, pyqtSignal

class LightDarkModeManager(QObject):
    """
    Dịch vụ quản lý Chế độ Sáng/Tối (Light/Dark Mode) độc lập.
    Quản lý trạng thái "sáng" hoặc "tối" (light/dark) độc lập với Style Theme.
    """
    mode_changed = pyqtSignal(str)  # Phát đi "light" hoặc "dark"

    def __init__(self, default_mode: str = "dark"):
        super().__init__()
        self._current_mode = default_mode if default_mode in ["light", "dark"] else "dark"

    def get_current_mode(self) -> str:
        return self._current_mode

    def is_dark(self) -> bool:
        return self._current_mode == "dark"

    def switch_mode(self, mode: str):
        if mode not in ["light", "dark"]:
            return
        if self._current_mode != mode:
            self._current_mode = mode
            self.mode_changed.emit(mode)
