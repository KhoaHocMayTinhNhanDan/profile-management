from ..abstract.i_buttons_product import AbstractButtons

class Qt6Buttons(AbstractButtons):
    def get_template(self) -> str:
        return '''from PyQt6.QtWidgets import QPushButton

class PrimaryButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #89b4fa;
                color: #11111b;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 6px;
                border: none;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #b4befe;
            }
        """)

class DangerButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #f38ba8;
                color: #11111b;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 6px;
                border: none;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #ff9999;
            }
        """)

class SecondaryButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #313244;
                color: #cdd6f4;
                padding: 10px 20px;
                border-radius: 6px;
                border: 1px solid #45475a;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #45475a;
            }
        """)
'''
