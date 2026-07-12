from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont


class HeaderLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        self.setProperty("class", "HeaderLabel")
        self.setObjectName("header_lbl")


class BodyLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Inter", 11))
        self.setProperty("class", "BodyLabel")
        self.setObjectName("body_lbl")


from PyQt6.QtCore import Qt
from typing import Any


class ClickableLabel(QLabel):
    """Custom QLabel that executes a callback on left click, styled as an interactive link."""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.callback: Any = None
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, ev):
        if (
            ev is not None
            and ev.button() == Qt.MouseButton.LeftButton
            and self.callback
        ):
            self.callback()
        super().mousePressEvent(ev)
