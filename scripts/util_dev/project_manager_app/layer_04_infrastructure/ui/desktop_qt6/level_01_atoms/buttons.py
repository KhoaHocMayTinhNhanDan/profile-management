from PyQt6.QtWidgets import QPushButton

class PrimaryButton(QPushButton):
    """
    PrimaryButton - Nút bấm hành động chính.
    Toàn bộ style (màu sắc, viền, hiệu ứng hover) được định nghĩa tập trung ở ThemeManager QSS.
    """
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setProperty("class", "PrimaryButton")


class NavButton(QPushButton):
    """
    NavButton - Nút điều hướng Sidebar.
    """
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setProperty("class", "NavButton")


class SecondaryButton(QPushButton):
    """
    SecondaryButton - Nút phụ.
    """
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setProperty("class", "SecondaryButton")
