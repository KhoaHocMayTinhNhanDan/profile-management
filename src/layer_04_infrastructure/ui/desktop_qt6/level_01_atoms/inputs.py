from PyQt6.QtWidgets import QLineEdit, QComboBox


class FormLineEdit(QLineEdit):
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setProperty("class", "FormLineEdit")
        self.setObjectName("form_input")


class FormComboBox(QComboBox):
    def __init__(self, items=None, parent=None):
        super().__init__(parent)
        if items:
            self.addItems(items)
        self.setProperty("class", "FormComboBox")
        self.setObjectName("form_combo")
