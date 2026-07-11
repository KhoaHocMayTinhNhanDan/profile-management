from ..abstract.i_inputs_product import AbstractInputs


class Qt6Inputs(AbstractInputs):
    def get_template(self) -> str:
        return '''from PyQt6.QtWidgets import QLineEdit, QComboBox

class FormLineEdit(QLineEdit):
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                background-color: #181825;
                color: #cdd6f4;
                border: 1px solid #313244;
                border-radius: 6px;
                padding: 10px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #89b4fa;
            }
        """)

class FormComboBox(QComboBox):
    def __init__(self, items=None, parent=None):
        super().__init__(parent)
        if items:
            self.addItems(items)
        self.setStyleSheet("""
            QComboBox {
                background-color: #181825;
                color: #cdd6f4;
                border: 1px solid #313244;
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
            }
        """)
'''
