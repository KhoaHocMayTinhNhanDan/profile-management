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
