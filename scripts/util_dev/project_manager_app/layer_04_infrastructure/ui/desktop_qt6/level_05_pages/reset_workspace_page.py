from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from ..level_01_atoms.labels import SubtitleLabel, BodyLabel
from ..level_02_molecules.notification_dialog import NotificationDialog
from ..level_01_atoms.buttons import PrimaryButton
from ..level_04_templates.page_template import BasePageTemplate

class ResetWorkspacePage(BasePageTemplate):
    """
    ResetWorkspacePage - Trang xóa sạch workspace làm việc.
    Kế thừa BasePageTemplate để đồng bộ i18n và theme động 100%.
    """
    def __init__(self, main_win, app_ctx):
        super().__init__("Danger Zone", app_ctx)
        self.main_win = main_win
        
        self.warning_card = QFrame()
        self.warning_card.setObjectName("warning_card")
        self.warn_layout = QVBoxLayout(self.warning_card)
        self.warn_layout.setContentsMargins(30, 30, 30, 30)
        self.warn_layout.setSpacing(20)
        
        self.warn_icon = QLabel("⚠️")
        self.warn_icon.setFont(QFont("Inter", 48))
        self.warn_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.warn_layout.addWidget(self.warn_icon)
        
        self.warn_title = SubtitleLabel("DANGER ZONE: ERASE ENTIRE WORKSPACE")
        self.warn_title.setObjectName("lbl_danger_title")
        self.warn_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.warn_layout.addWidget(self.warn_title)
        
        self.warn_desc = BodyLabel(
            "This operation will wipe all files in src/ and tests/."
        )
        self.warn_desc.setFont(QFont("Inter", 12))
        self.warn_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.warn_desc.setWordWrap(True)
        self.warn_layout.addWidget(self.warn_desc)
        
        self.content_layout.addWidget(self.warning_card)
        
        actions_box = QHBoxLayout()
        actions_box.addStretch()
        
        self.reset_btn = PrimaryButton("🧹 Erase Workspace")
        self.reset_btn.setObjectName("danger_btn")  # Sử dụng ID selector của QSS
        self.reset_btn.clicked.connect(self.handle_reset_workspace)
        actions_box.addWidget(self.reset_btn)
        self.content_layout.addLayout(actions_box)
        
        self.content_layout.addStretch()

    def handle_reset_workspace(self):
        reply = NotificationDialog.ask_question(self, 'Reset Workspace', 
            'CRITICAL WARNING: This will permanently delete all code files in src/ and tests/.\n\nAre you absolutely sure?')
        
        if reply:
            self.main_win.log_info("Cleaning workspace...")
            success = self.app_ctx.reset_controller.execute()
            if success:
                self.main_win.log_success("Workspace successfully wiped clean.")
                if hasattr(self.main_win, 'on_workspace_reset'):
                    self.main_win.on_workspace_reset()
            else:
                self.main_win.log_error("Workspace clean failed.")

    def retranslate_ui(self, lang_code: str):
        self.warn_title.setText(self.i18n_manager.translate("⚠️ Erase Workspace"))
        self.warn_desc.setText(self.i18n_manager.translate("This operation will wipe all files in src/ and tests/."))
        self.reset_btn.setText(self.i18n_manager.translate("🔥 WIPE WORKSPACE"))
        
