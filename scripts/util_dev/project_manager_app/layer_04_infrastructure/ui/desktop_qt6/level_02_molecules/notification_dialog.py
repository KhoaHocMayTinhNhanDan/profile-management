from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ..theme import DARK_BG, CARD_BG, BORDER_COLOR, TEXT_COLOR
from ..level_01_atoms.labels import BodyLabel
from ..level_01_atoms.buttons import PrimaryButton

class NotificationDialog(QDialog):
    """
    Hộp thoại thông báo tùy chỉnh (Custom Message/Question Dialog).
    Là một Molecule được thiết kế hoàn toàn theo Atomic Design để thay thế QMessageBox.
    """
    def __init__(self, title, message, is_question=False, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Tạo viền ngoài bo góc cao cấp
        self.frame = QFrame()
        self.frame.setStyleSheet(f"""
            QFrame {{
                background-color: {DARK_BG};
                border: 2px solid {BORDER_COLOR};
                border-radius: 12px;
            }}
        """)
        
        frame_layout = QVBoxLayout(self.frame)
        frame_layout.setContentsMargins(25, 25, 25, 20)
        frame_layout.setSpacing(20)
        
        # Nhãn nội dung thông báo (Atom)
        self.message_label = BodyLabel(message)
        self.message_label.setFont(QFont("Inter", 12))
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet(f"color: {TEXT_COLOR}; border: none; background: transparent;")
        frame_layout.addWidget(self.message_label)
        
        # Nút xác nhận OK hoặc Yes/No (Atom)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        if is_question:
            # Yes Button (Primary style)
            self.yes_button = PrimaryButton("Yes")
            self.yes_button.setFixedWidth(90)
            self.yes_button.clicked.connect(self.accept)
            
            # No Button (Secondary outline style)
            from ..level_01_atoms.buttons import QPushButton
            self.no_button = QPushButton("No")
            self.no_button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {CARD_BG};
                    color: {TEXT_COLOR};
                    border: 1px solid {BORDER_COLOR};
                    border-radius: 6px;
                    padding: 10px;
                    font-weight: bold;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: {BORDER_COLOR};
                }}
            """)
            self.no_button.setFixedWidth(90)
            self.no_button.clicked.connect(self.reject)
            
            btn_layout.addWidget(self.yes_button)
            btn_layout.addWidget(self.no_button)
        else:
            self.ok_button = PrimaryButton("OK")
            self.ok_button.setFixedWidth(100)
            self.ok_button.clicked.connect(self.accept)
            btn_layout.addWidget(self.ok_button)
            
        btn_layout.addStretch()
        frame_layout.addLayout(btn_layout)
        
        # Base Layout của Dialog
        base_layout = QVBoxLayout(self)
        base_layout.setContentsMargins(0, 0, 0, 0)
        base_layout.addWidget(self.frame)

    @staticmethod
    def show_message(parent, title, message):
        """Helper tĩnh để hiển thị thông báo nhanh tương tự QMessageBox.information."""
        dialog = NotificationDialog(title, message, is_question=False, parent=parent)
        dialog.exec()

    @staticmethod
    def ask_question(parent, title, message) -> bool:
        """Helper tĩnh để hiển thị hộp thoại xác nhận Yes/No tương tự QMessageBox.question. Trả về True nếu chọn Yes."""
        dialog = NotificationDialog(title, message, is_question=True, parent=parent)
        result = dialog.exec()
        return result == QDialog.DialogCode.Accepted

