from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLabel,
    QListWidget,
    QListWidgetItem,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ..theme import (
    DARK_BG,
    CARD_BG,
    BORDER_COLOR,
    TEXT_COLOR,
    ACCENT_COLOR,
    SUBTEXT_COLOR,
    SUCCESS_COLOR,
    ERROR_COLOR,
)
from ..level_01_atoms.labels import HeaderLabel, SubtitleLabel, BodyLabel
from ..level_01_atoms.inputs import FormLineEdit
from ..level_01_atoms.buttons import PrimaryButton, SecondaryButton
from ..level_02_molecules.notification_dialog import NotificationDialog
from scripts.util_dev.project_manager_app.config.project_config import (
    write_project_name,
)


class WelcomePage(QDialog):
    """
    Dialog chào mừng - hiển thị khi workspace chưa có project nào được kích hoạt.
    Bắt buộc người dùng tạo project mới hoặc load project cũ trước khi vào main window.
    """

    def __init__(self, parent, app_ctx, root_dir):
        super().__init__(parent)
        self.app_ctx = app_ctx
        self.root_dir = root_dir

        self.setWindowTitle("Welcome — Setup Project")
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setModal(True)
        self.resize(520, 500)

        # Outer frame
        self.frame = QFrame(self)
        self.frame.setGeometry(0, 0, 520, 500)
        self.frame.setStyleSheet(f"""
            QFrame {{
                background-color: {DARK_BG};
                border: 2px solid {BORDER_COLOR};
                border-radius: 16px;
            }}
        """)

        layout = QVBoxLayout(self.frame)
        layout.setContentsMargins(35, 35, 35, 30)
        layout.setSpacing(20)

        # Title
        title = QLabel("🛠️  Clean Architecture Project Manager")
        title.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        title.setStyleSheet(
            f"color: {ACCENT_COLOR}; border: none; background: transparent;"
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel(
            "Chưa có project nào đang hoạt động trong workspace.\nHãy tạo project mới hoặc load project đã lưu để bắt đầu."
        )
        subtitle.setFont(QFont("Inter", 10))
        subtitle.setStyleSheet(
            f"color: {SUBTEXT_COLOR}; border: none; background: transparent;"
        )
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet(
            f"color: {BORDER_COLOR}; border: none; background: {BORDER_COLOR}; max-height: 1px;"
        )
        layout.addWidget(line)

        # --- NEW PROJECT CARD ---
        new_card = QFrame()
        new_card.setStyleSheet(f"""
            QFrame {{
                background-color: {CARD_BG};
                border: 1px solid {BORDER_COLOR};
                border-radius: 10px;
            }}
            QLabel {{ border: none; background: transparent; }}
        """)
        new_layout = QVBoxLayout(new_card)
        new_layout.setContentsMargins(20, 18, 20, 18)
        new_layout.setSpacing(12)

        new_title = QLabel("✨  Tạo Project Mới")
        new_title.setFont(QFont("Inter", 11, QFont.Weight.Bold))
        new_title.setStyleSheet(f"color: {ACCENT_COLOR};")
        new_layout.addWidget(new_title)

        self.new_proj_input = FormLineEdit(
            "Tên project (VD: trading_bot, ecommerce_api...)"
        )
        new_layout.addWidget(self.new_proj_input)

        create_btn = PrimaryButton("🚀 Tạo Project")
        create_btn.clicked.connect(self.handle_create)
        new_layout.addWidget(create_btn)
        layout.addWidget(new_card)

        # --- LOAD PROJECT CARD ---
        load_card = QFrame()
        load_card.setStyleSheet(f"""
            QFrame {{
                background-color: {CARD_BG};
                border: 1px solid {BORDER_COLOR};
                border-radius: 10px;
            }}
            QLabel {{ border: none; background: transparent; }}
        """)
        load_layout = QVBoxLayout(load_card)
        load_layout.setContentsMargins(20, 18, 20, 18)
        load_layout.setSpacing(12)

        load_title = QLabel("📂  Load Project Đã Lưu")
        load_title.setFont(QFont("Inter", 11, QFont.Weight.Bold))
        load_title.setStyleSheet(f"color: {SUCCESS_COLOR};")
        load_layout.addWidget(load_title)

        self.project_list = QListWidget()
        self.project_list.setMaximumHeight(100)
        self.project_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {DARK_BG};
                border: 1px solid {BORDER_COLOR};
                border-radius: 6px;
                color: {TEXT_COLOR};
                padding: 4px;
            }}
            QListWidget::item {{ padding: 6px 10px; border-radius: 4px; }}
            QListWidget::item:selected {{ background-color: {BORDER_COLOR}; color: {ACCENT_COLOR}; }}
        """)
        self._load_saved_projects()
        load_layout.addWidget(self.project_list)

        load_btn = SecondaryButton("📂 Load & Kích hoạt")
        load_btn.clicked.connect(self.handle_load)
        load_layout.addWidget(load_btn)
        layout.addWidget(load_card)

    def _load_saved_projects(self):
        self.project_list.clear()
        try:
            projs = self.app_ctx.list_controller.execute()
            if not projs:
                item = QListWidgetItem("(Chưa có project nào được lưu)")
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                item.setForeground(Qt.GlobalColor.gray)
                self.project_list.addItem(item)
            else:
                for p in projs:
                    self.project_list.addItem(p)
        except Exception:
            pass

    def handle_create(self):
        name = self.new_proj_input.text().strip()
        if not name:
            NotificationDialog.show_message(
                self, "Warning", "Tên project không được để trống!"
            )
            return
        if write_project_name(self.root_dir, name):
            self.accept()
        else:
            NotificationDialog.show_message(
                self, "Error", "Không thể lưu cấu hình project!"
            )

    def handle_load(self):
        selected = self.project_list.currentItem()
        if not selected or not selected.flags() & Qt.ItemFlag.ItemIsSelectable:
            NotificationDialog.show_message(
                self, "Warning", "Hãy chọn một project từ danh sách!"
            )
            return
        text = selected.text()
        import os

        src_dir = os.path.join(self.root_dir, "src")
        tests_dir = os.path.join(self.root_dir, "tests")
        ok = self.app_ctx.load_controller.execute(text, src_dir, tests_dir)
        if ok:
            write_project_name(self.root_dir, text)
            self.accept()
        else:
            NotificationDialog.show_message(
                self, "Error", f"Không thể load project '{text}'!"
            )
