from PyQt6.QtWidgets import QLineEdit, QCheckBox


class FormLineEdit(QLineEdit):
    """
    FormLineEdit - Ô nhập liệu chuẩn.
    """

    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setProperty("class", "FormLineEdit")


class FormCheckBox(QCheckBox):
    """
    FormCheckBox - Hộp kiểm chuẩn.
    """

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setProperty("class", "FormCheckBox")
