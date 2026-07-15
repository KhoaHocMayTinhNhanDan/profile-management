import os
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QListWidget,
    QListWidgetItem,
)
from PyQt6.QtCore import Qt
from ..level_01_atoms.labels import SubtitleLabel, BodyLabel
from ..level_01_atoms.inputs import FormLineEdit
from ..level_02_molecules import NotificationDialog

from ..level_01_atoms.buttons import PrimaryButton, SecondaryButton
from ..level_04_templates.page_template import BasePageTemplate


class SavedProjectsPage(BasePageTemplate):
    """
    SavedProjectsPage - Trang sao lưu và phục hồi dự án.
    Kế thừa BasePageTemplate để đồng bộ i18n và theme động 100%.
    """

    def __init__(self, main_win, app_ctx, root_dir):
        super().__init__("Backup / Restore", app_ctx)
        self.main_win = main_win
        self.root_dir = root_dir

        # Grid layout for Save (left) and Load (right) cards
        grid = QHBoxLayout()
        grid.setSpacing(20)

        # 1. SAVE CARD
        save_card = QFrame()
        save_card.setObjectName("save_card")
        save_layout = QVBoxLayout(save_card)
        save_layout.setContentsMargins(20, 20, 20, 20)
        save_layout.setSpacing(15)

        self.save_title = SubtitleLabel("Backup Current Workspace")
        self.save_title.setObjectName("lbl_new_title")  # Lấy style accent
        save_layout.addWidget(self.save_title)

        self.save_desc = BodyLabel(
            "Saves src/ and tests/ folders into a named backup archive."
        )
        self.save_desc.setWordWrap(True)
        save_layout.addWidget(self.save_desc)

        self.save_name_input = FormLineEdit("Backup name (e.g. trading_bot_v1)")
        proj = (
            self.main_win.get_project_name()
            if hasattr(self.main_win, "get_project_name")
            else ""
        )
        if proj:
            self.save_name_input.setText(proj)
        save_layout.addWidget(self.save_name_input)

        self.save_btn = SecondaryButton("💾 Backup Now")
        self.save_btn.clicked.connect(self.handle_save_project)
        save_layout.addWidget(self.save_btn)
        save_layout.addStretch()
        grid.addWidget(save_card, stretch=1)

        # 2. LOAD CARD
        load_card = QFrame()
        load_card.setObjectName("load_card")
        load_layout = QVBoxLayout(load_card)
        load_layout.setContentsMargins(20, 20, 20, 20)
        load_layout.setSpacing(15)

        self.load_title = SubtitleLabel("Recover Stored Backups")
        self.load_title.setObjectName("lbl_load_title")  # Lấy style success
        load_layout.addWidget(self.load_title)

        self.project_list = QListWidget()
        load_layout.addWidget(self.project_list)

        btn_layout = QHBoxLayout()
        self.load_btn = PrimaryButton("📂 Restore Selection")
        self.load_btn.clicked.connect(self.handle_load_project)
        self.delete_btn = SecondaryButton("❌ Delete Selection")
        self.delete_btn.clicked.connect(self.handle_delete_project)
        btn_layout.addWidget(self.load_btn)
        btn_layout.addWidget(self.delete_btn)
        load_layout.addLayout(btn_layout)
        grid.addWidget(load_card, stretch=1)

        self.content_layout.addLayout(grid)
        self.refresh_project_list()

    def refresh_project_list(self):
        self.project_list.clear()
        if hasattr(self.main_win, "get_project_name"):
            proj = self.main_win.get_project_name()
            if proj and not self.save_name_input.text():
                self.save_name_input.setText(proj)
        try:
            projs = self.app_ctx.list_controller.execute()
            if not projs:
                placeholder = QListWidgetItem(
                    self.i18n_manager.translate("(No saved projects found)")
                )
                placeholder.setFlags(
                    placeholder.flags() & ~Qt.ItemFlag.ItemIsSelectable
                )
                placeholder.setForeground(Qt.GlobalColor.gray)
                self.project_list.addItem(placeholder)
            else:
                for p in projs:
                    self.project_list.addItem(p)
        except Exception as e:
            self.main_win.log_error(f"Failed to fetch projects: {str(e)}")

    def handle_save_project(self):
        text = self.save_name_input.text().strip()
        if not text:
            self.main_win.log_error("Backup name cannot be empty!")
            return

        src_dir = os.path.join(self.root_dir, "src")
        tests_dir = os.path.join(self.root_dir, "tests")

        self.main_win.log_info(f"Saving project state as '{text}'...")
        success = self.app_ctx.save_controller.execute(text, src_dir, tests_dir)
        if success:
            self.main_win.log_success(f"Project '{text}' successfully backed up.")
            self.save_name_input.clear()
            self.refresh_project_list()
        else:
            self.main_win.log_error("Project backup failed.")

    def handle_load_project(self):
        selected_item = self.project_list.currentItem()
        if (
            not selected_item
            or not selected_item.flags() & Qt.ItemFlag.ItemIsSelectable
        ):
            self.main_win.log_error("Select a project from the list to restore!")
            return

        text = selected_item.text()
        reply = NotificationDialog.ask_question(
            self,
            "Confirm Restore",
            f"Are you sure you want to load '{text}'? Current unsaved work in src/ and tests/ will be overwritten.",
        )

        if reply:
            src_dir = os.path.join(self.root_dir, "src")
            tests_dir = os.path.join(self.root_dir, "tests")
            self.main_win.log_info(f"Restoring project state to '{text}'...")
            success = self.app_ctx.load_controller.execute(text, src_dir, tests_dir)
            if success:
                if hasattr(self.main_win, "set_project_name"):
                    self.main_win.set_project_name(text)
                self.main_win.log_success(f"Project restored to '{text}' successfully.")
            else:
                self.main_win.log_error("Failed to restore project.")

    def handle_delete_project(self):
        selected_item = self.project_list.currentItem()
        if (
            not selected_item
            or not selected_item.flags() & Qt.ItemFlag.ItemIsSelectable
        ):
            self.main_win.log_error("Select a project from the list to delete!")
            return

        text = selected_item.text()
        reply = NotificationDialog.ask_question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete '{text}'? This operation cannot be undone.",
        )

        if reply:
            self.main_win.log_info(f"Deleting project '{text}'...")
            success = self.app_ctx.delete_controller.execute(text)
            if success:
                self.main_win.log_success(f"Project '{text}' deleted successfully.")
                self.refresh_project_list()
            else:
                self.main_win.log_error("Failed to delete project.")

    def retranslate_ui(self, lang_code: str):
        self.save_title.setText(self.i18n_manager.translate("Backup current workspace"))
        self.save_desc.setText(
            self.i18n_manager.translate(
                "This operation will back up src/ and tests/ folders."
            )
        )
        self.save_name_input.setPlaceholderText(
            self.i18n_manager.translate("Backup name (e.g. trading_bot_v1)")
        )
        self.save_btn.setText(
            self.i18n_manager.translate("📦 Backup current workspace")
        )
        self.load_title.setText(self.i18n_manager.translate("Saved Backups:"))
        self.load_btn.setText(self.i18n_manager.translate("📂 Restore Selected Backup"))
        self.delete_btn.setText(
            self.i18n_manager.translate("❌ Delete Selected Backup")
        )
        self.refresh_project_list()
