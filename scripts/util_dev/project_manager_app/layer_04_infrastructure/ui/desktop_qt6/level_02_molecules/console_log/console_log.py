from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
)
from PyQt6.QtGui import QFont


class LogConsole(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("log_console_frame")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)

        header = QHBoxLayout()
        title = QLabel("⚙️ SYSTEM OUTPUT LOG")
        title.setObjectName("log_console_title")
        title.setFont(QFont("Consolas", 10, QFont.Weight.Bold))
        header.addWidget(title)

        clear_btn = QPushButton("Clear")
        clear_btn.setObjectName("log_console_clear_btn")
        clear_btn.setFixedWidth(50)
        clear_btn.clicked.connect(self.clear_logs)
        header.addWidget(clear_btn)
        layout.addLayout(header)

        self.console = QTextEdit()
        self.console.setObjectName("log_console_textarea")
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Consolas", 11))
        self.console.setPlaceholderText(
            "Logs from generation and checks will display here..."
        )
        layout.addWidget(self.console)

    def append_log(self, text):
        self.console.append(text)

    def clear_logs(self):
        self.console.clear()
