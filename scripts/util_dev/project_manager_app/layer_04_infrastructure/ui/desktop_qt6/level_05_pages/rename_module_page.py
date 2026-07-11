from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLabel,
    QLineEdit,
    QGridLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from ..level_01_atoms.buttons import PrimaryButton
from ..level_04_templates.page_template import BasePageTemplate


class RenameModulePage(BasePageTemplate):
    """
    RenameModulePage - Trang Refactor Module gộp cả 2 tính năng:
    1. Rename Module (Đổi tên tại chỗ)
    2. Move Module (Cut & Paste sang thư mục khác)
    Thiết kế 2 Card nằm ngang hiện đại.
    """

    def __init__(self, main_win, app_ctx, root_dir):
        super().__init__("Refactor Module", app_ctx)
        self.main_win = main_win
        self.root_dir = root_dir

        # Main Layout sử dụng Grid Layout cho 2 cards
        grid_layout = QGridLayout()
        grid_layout.setSpacing(25)

        # ----------------------------------------------------
        # CARD 1: RENAME MODULE (Left)
        # ----------------------------------------------------
        self.card_rename = QFrame()
        self.card_rename.setObjectName("utility_card")
        self.card_rename.setProperty("class", "InteractiveCard")
        layout_rename = QVBoxLayout(self.card_rename)
        layout_rename.setContentsMargins(25, 25, 25, 25)
        layout_rename.setSpacing(12)

        self.lbl_rename_icon = QLabel("🔄")
        self.lbl_rename_icon.setFont(QFont("Inter", 32))
        self.lbl_rename_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_rename_title = QLabel("Rename Module")
        self.lbl_rename_title.setFont(QFont("Inter", 12, QFont.Weight.Bold))
        self.lbl_rename_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_rename_title.setProperty("class", "HeaderLabel")

        self.lbl_rename_target = QLabel("Target Module / Folder Path:")
        self.lbl_rename_target.setFont(QFont("Inter", 9, QFont.Weight.Bold))
        self.lbl_rename_target.setProperty("class", "BodyLabel")
        self.txt_rename_target = QLineEdit()
        self.txt_rename_target.setPlaceholderText(
            "e.g. src/layer_01_entities/old_name.py"
        )

        self.lbl_rename_new = QLabel("New Name:")
        self.lbl_rename_new.setFont(QFont("Inter", 9, QFont.Weight.Bold))
        self.lbl_rename_new.setProperty("class", "BodyLabel")
        self.txt_rename_new = QLineEdit()
        self.txt_rename_new.setPlaceholderText("e.g. new_name")

        self.btn_rename = PrimaryButton("Rename Module")
        self.btn_rename.clicked.connect(self.handle_rename)

        layout_rename.addWidget(self.lbl_rename_icon)
        layout_rename.addWidget(self.lbl_rename_title)
        layout_rename.addWidget(self.lbl_rename_target)
        layout_rename.addWidget(self.txt_rename_target)
        layout_rename.addWidget(self.lbl_rename_new)
        layout_rename.addWidget(self.txt_rename_new)
        layout_rename.addStretch()
        layout_rename.addWidget(self.btn_rename)

        # ----------------------------------------------------
        # CARD 2: MOVE MODULE (Right - Cut & Paste)
        # ----------------------------------------------------
        self.card_move = QFrame()
        self.card_move.setObjectName("utility_card")
        self.card_move.setProperty("class", "InteractiveCard")
        layout_move = QVBoxLayout(self.card_move)
        layout_move.setContentsMargins(25, 25, 25, 25)
        layout_move.setSpacing(12)

        self.lbl_move_icon = QLabel("✂️")
        self.lbl_move_icon.setFont(QFont("Inter", 32))
        self.lbl_move_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_move_title = QLabel("Move Module (Cut & Paste)")
        self.lbl_move_title.setFont(QFont("Inter", 12, QFont.Weight.Bold))
        self.lbl_move_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_move_title.setProperty("class", "HeaderLabel")

        self.lbl_move_source = QLabel("Source Module / Folder Path:")
        self.lbl_move_source.setFont(QFont("Inter", 9, QFont.Weight.Bold))
        self.lbl_move_source.setProperty("class", "BodyLabel")
        self.txt_move_source = QLineEdit()
        self.txt_move_source.setPlaceholderText(
            "e.g. src/layer_01_entities/old_name.py"
        )

        self.lbl_move_dest = QLabel("Destination Directory Path:")
        self.lbl_move_dest.setFont(QFont("Inter", 9, QFont.Weight.Bold))
        self.lbl_move_dest.setProperty("class", "BodyLabel")
        self.txt_move_dest = QLineEdit()
        self.txt_move_dest.setPlaceholderText("e.g. src/layer_02_usecases")

        self.btn_move = PrimaryButton("Move & Paste Module")
        self.btn_move.clicked.connect(self.handle_move)

        layout_move.addWidget(self.lbl_move_icon)
        layout_move.addWidget(self.lbl_move_title)
        layout_move.addWidget(self.lbl_move_source)
        layout_move.addWidget(self.txt_move_source)
        layout_move.addWidget(self.lbl_move_dest)
        layout_move.addWidget(self.txt_move_dest)
        layout_move.addStretch()
        layout_move.addWidget(self.btn_move)

        # Add cards to layout
        grid_layout.addWidget(self.card_rename, 0, 0)
        grid_layout.addWidget(self.card_move, 0, 1)

        self.content_layout.addLayout(grid_layout)
        self.content_layout.addStretch()

    def handle_rename(self):
        target = self.txt_rename_target.text().strip()
        new_name = self.txt_rename_new.text().strip()

        if not target or not new_name:
            self.main_win.log_error("Please fill in both Target Path and New Name.")
            return

        self.main_win.log_info(
            f"Starting refactoring rename: '{target}' -> '{new_name}'..."
        )
        res = self.app_ctx.rename_module_controller.execute(target, new_name)

        if res.success:
            self.main_win.log_success(res.message)
            self.txt_rename_target.clear()
            self.txt_rename_new.clear()
        else:
            self.main_win.log_error(res.message)

    def handle_move(self):
        source = self.txt_move_source.text().strip()
        dest = self.txt_move_dest.text().strip()

        if not source or not dest:
            self.main_win.log_error(
                "Please fill in both Source Path and Destination Folder."
            )
            return

        self.main_win.log_info(
            f"Starting refactoring move (cut & paste): '{source}' -> '{dest}'..."
        )
        res = self.app_ctx.move_module_controller.execute(source, dest)

        if res.success:
            self.main_win.log_success(res.message)
            self.txt_move_source.clear()
            self.txt_move_dest.clear()
        else:
            self.main_win.log_error(res.message)

    def retranslate_ui(self, lang_code: str):
        self.lbl_rename_title.setText(self.i18n_manager.translate("Rename Module"))
        self.lbl_rename_target.setText(
            self.i18n_manager.translate("Target Module / Folder Path:")
        )
        self.lbl_rename_new.setText(self.i18n_manager.translate("New Name:"))
        self.btn_rename.setText(self.i18n_manager.translate("Rename Module"))

        self.lbl_move_title.setText(
            self.i18n_manager.translate("Move Module (Cut & Paste)")
        )
        self.lbl_move_source.setText(
            self.i18n_manager.translate("Source Module / Folder Path:")
        )
        self.lbl_move_dest.setText(
            self.i18n_manager.translate("Destination Directory Path:")
        )
        self.btn_move.setText(self.i18n_manager.translate("Move & Paste Module"))
