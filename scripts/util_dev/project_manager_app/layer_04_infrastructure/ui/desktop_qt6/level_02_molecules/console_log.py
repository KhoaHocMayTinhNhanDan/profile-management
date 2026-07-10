from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from ..theme import SIDEBAR_BG, BORDER_COLOR, SUBTEXT_COLOR, ERROR_COLOR, SUCCESS_COLOR

class LogConsole(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {SIDEBAR_BG};
                border: 1px solid {BORDER_COLOR};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        
        header = QHBoxLayout()
        title = QLabel("⚙️ SYSTEM OUTPUT LOG")
        title.setFont(QFont("Consolas", 10, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {SUBTEXT_COLOR}; border: none;")
        header.addWidget(title)
        
        clear_btn = QPushButton("Clear")
        clear_btn.setFixedWidth(50)
        clear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {SUBTEXT_COLOR};
                border: none;
                font-size: 11px;
            }}
            QPushButton:hover {{
                color: {ERROR_COLOR};
            }}
        """)
        clear_btn.clicked.connect(self.clear_logs)
        header.addWidget(clear_btn)
        layout.addLayout(header)
        
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Consolas", 11))
        self.console.setStyleSheet(f"""
            QTextEdit {{
                background-color: #0c0c12;
                color: {SUCCESS_COLOR};
                border: none;
                border-radius: 4px;
                padding: 8px;
            }}
            QTextEdit::placeholder {{
                color: {SUBTEXT_COLOR};
            }}
        """)
        self.console.setPlaceholderText("Logs from generation and checks will display here...")
        layout.addWidget(self.console)
        
    def append_log(self, text):
        self.console.append(text)
        
    def clear_logs(self):
        self.console.clear()
