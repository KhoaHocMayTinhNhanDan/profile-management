from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont


class HeaderLabel(QLabel):
    """
    HeaderLabel - Tiêu đề trang chính lớn.
    """

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Inter", 22, QFont.Weight.Bold))
        self.setProperty("class", "HeaderLabel")


class SubtitleLabel(QLabel):
    """
    SubtitleLabel - Tiêu đề phụ.
    """

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        self.setProperty("class", "SubtitleLabel")


class BodyLabel(QLabel):
    """
    BodyLabel - Văn bản thường.
    """

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont("Inter", 10, QFont.Weight.Medium))
        self.setProperty("class", "BodyLabel")
