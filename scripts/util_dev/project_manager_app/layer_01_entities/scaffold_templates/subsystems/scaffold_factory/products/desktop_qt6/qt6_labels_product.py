from ..abstract.i_labels_product import AbstractLabels

class Qt6Labels(AbstractLabels):
    def get_template(self) -> str:
        return '''from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont

class HeaderLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        self.setStyleSheet("color: #89b4fa; margin-bottom: 10px;")

class BodyLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Inter", 11))
        self.setStyleSheet("color: #cdd6f4;")
'''
