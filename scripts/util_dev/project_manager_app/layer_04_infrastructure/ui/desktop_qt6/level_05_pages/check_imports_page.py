from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from ..level_01_atoms.buttons import PrimaryButton
from ..level_04_templates.page_template import BasePageTemplate

class CheckImportsPage(BasePageTemplate):
    """
    CheckImportsPage - Trang quét luật dependency import của Clean Architecture.
    Kế thừa BasePageTemplate để đồng bộ i18n và theme động 100%.
    """
    def __init__(self, main_win, app_ctx, root_dir):
        super().__init__("Check Architecture", app_ctx)
        self.main_win = main_win
        self.root_dir = root_dir
        
        self.status_card = QFrame()
        self.status_card.setObjectName("status_card")
        self.status_layout = QVBoxLayout(self.status_card)
        self.status_layout.setContentsMargins(30, 30, 30, 30)
        self.status_layout.setSpacing(15)
        
        self.status_icon = QLabel("🛡️")
        self.status_icon.setFont(QFont("Inter", 48))
        self.status_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.status_text = QLabel("Press Scan to check Clean Architecture import rules.")
        self.status_text.setFont(QFont("Inter", 14, QFont.Weight.Bold))
        self.status_text.setObjectName("status_text")
        self.status_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_text.setWordWrap(True)
        
        self.status_layout.addWidget(self.status_icon)
        self.status_layout.addWidget(self.status_text)
        self.content_layout.addWidget(self.status_card)
        
        actions_box = QHBoxLayout()
        actions_box.addStretch()
        
        self.scan_btn = PrimaryButton("🔍 Run Scan")
        self.scan_btn.clicked.connect(self.handle_check_imports)
        actions_box.addWidget(self.scan_btn)
        self.content_layout.addLayout(actions_box)
        
        self.content_layout.addStretch()

    def handle_check_imports(self):
        self.main_win.log_info("Running static import dependency scan...")
        output = self.app_ctx.check_imports_controller.execute(self.root_dir)
        
        if output.status == "error":
            self.status_icon.setText("⚠️")
            self.status_text.setText("Architecture Rules Violated!")
            self.status_text.setProperty("theme_status", "error")
            
            for v in output.violations:
                line = f"Violation: {v[0]} (Layer {v[1]} imports Layer {v[2]})"
                self.main_win.log_error(line)
        else:
            self.status_icon.setText("🛡️")
            self.status_text.setText("Clean Architecture is Clean!")
            self.status_text.setProperty("theme_status", "success")
            self.main_win.log_success("Import dependency scan: All layer boundaries are clean.")
            
        self.status_text.style().unpolish(self.status_text)
        self.status_text.style().polish(self.status_text)

    def retranslate_ui(self, lang_code: str):
        self.status_text.setText(self.i18n_manager.translate("Press Scan to check Clean Architecture import rules."))
        self.scan_btn.setText(self.i18n_manager.translate("🔍 Scan Architecture"))
