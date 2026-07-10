class DesktopQt5Factory:
    """
    Concrete Factory tạo UI templates cho Desktop PyQt5.
    """
    @staticmethod
    def get_ui_pyqt5_template(pascal_name: str, snake_name: str) -> str:
        return f'''
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class {pascal_name}Page(QWidget):
    def __init__(self, context):
        super().__init__()
        self.context = context
        
        layout = QVBoxLayout()
        lbl = QLabel("Màn hình {pascal_name} - PyQt5")
        btn = QPushButton("Thực thi {pascal_name}")
        
        layout.addWidget(lbl)
        layout.addWidget(btn)
        self.setLayout(layout)
'''
