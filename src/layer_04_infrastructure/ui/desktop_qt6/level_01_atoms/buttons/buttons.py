from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon


class PrimaryButton(QPushButton):

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setProperty("class", "PrimaryButton")
        self.setObjectName("primary_btn")
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class DangerButton(QPushButton):

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setProperty("class", "DangerButton")
        self.setObjectName("danger_btn")
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class SecondaryButton(QPushButton):

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setProperty("class", "SecondaryButton")
        self.setObjectName("secondary_btn")
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class NavButton(QPushButton):

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setProperty("class", "NavButton")
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class IconButton(QPushButton):

    def __init__(self, icon, parent=None):
        super().__init__(parent)
        if isinstance(icon, QIcon):
            self.setIcon(icon)
        elif isinstance(icon, str):
            self.setIcon(QIcon(icon))
        self.setIconSize(QSize(16, 16))
        self.setProperty("class", "IconButton")
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class TertiaryButton(QPushButton):

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setProperty("class", "TertiaryButton")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
