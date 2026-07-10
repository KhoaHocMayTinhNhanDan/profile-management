import sys
import io
import argparse
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QFrame
from PyQt6.QtGui import QFont
from ..level_01_atoms.labels import SubtitleLabel, BodyLabel
from ..level_01_atoms.inputs import FormLineEdit, FormCheckBox
from ..level_01_atoms.buttons import PrimaryButton
from ..level_02_molecules.notification_dialog import NotificationDialog
from ..level_04_templates.page_template import BasePageTemplate

class GeneratePage(BasePageTemplate):
    """
    GeneratePage - Trang tạo tính năng mới cho dự án.
    Kế thừa BasePageTemplate để đồng bộ i18n và theme động 100%.
    """
    def __init__(self, main_win, app_ctx, root_dir):
        super().__init__("Add Feature", app_ctx)
        self.main_win = main_win
        self.root_dir = root_dir
        
        # Card container
        self.card = QFrame()
        self.card.setObjectName("feature_card")
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(20)
        
        # Feature Name
        self.name_label = BodyLabel("Feature Name (CamelCase / PascalCase)")
        self.feature_name_input = FormLineEdit("e.g. PlaceOrder, UserAuth")
        
        card_layout.addWidget(self.name_label)
        card_layout.addWidget(self.feature_name_input)
        
        # Platforms selection
        self.plat_label = BodyLabel("Platforms / Presentation Channels")
        card_layout.addWidget(self.plat_label)
        
        platforms_box = QWidget()
        platforms_layout = QHBoxLayout(platforms_box)
        platforms_layout.setContentsMargins(0, 0, 0, 0)
        platforms_layout.setSpacing(15)
        
        self.plat_cb = {}
        for p in ["web", "desktop", "mobile", "cli"]:
            cb = FormCheckBox(p.upper())
            if p in ["web", "desktop"]:
                cb.setChecked(True)
            self.plat_cb[p] = cb
            platforms_layout.addWidget(cb)
        platforms_layout.addStretch()
        card_layout.addWidget(platforms_box)
        
        # Databases selection
        self.db_label = BodyLabel("Database Implementations (Layer 4)")
        card_layout.addWidget(self.db_label)
        
        dbs_box = QWidget()
        dbs_layout = QHBoxLayout(dbs_box)
        dbs_layout.setContentsMargins(0, 0, 0, 0)
        dbs_layout.setSpacing(15)
        
        self.db_cb = {}
        for db in ["sqlite", "postgres", "mongodb", "redis", "mock"]:
            cb = FormCheckBox(db.upper())
            if db == "sqlite":
                cb.setChecked(True)
            self.db_cb[db] = cb
            dbs_layout.addWidget(cb)
        dbs_layout.addStretch()
        card_layout.addWidget(dbs_box)
        
        self.content_layout.addWidget(self.card)
        
        # Action button
        actions_box = QHBoxLayout()
        actions_box.addStretch()
        
        self.generate_btn = PrimaryButton("🚀 Generate Feature")
        self.generate_btn.clicked.connect(self.handle_generate)
        actions_box.addWidget(self.generate_btn)
        self.content_layout.addLayout(actions_box)
        self.content_layout.addStretch()

    def handle_generate(self):
        name = self.feature_name_input.text().strip()
        if not name:
            NotificationDialog.show_message(self, "Warning", "Feature Name cannot be empty!")
            return
            
        platforms = [p for p, cb in self.plat_cb.items() if cb.isChecked()]
        db_techs = [db for db, cb in self.db_cb.items() if cb.isChecked()]
        
        if not platforms:
            NotificationDialog.show_message(self, "Warning", "Select at least one platform!")
            return
        if not db_techs:
            NotificationDialog.show_message(self, "Warning", "Select at least one DB implementation!")
            return
            
        args = argparse.Namespace(
            name=name,
            platforms=",".join(platforms),
            db=",".join(db_techs)
        )
        
        project_name = self.main_win.get_project_name() if hasattr(self.main_win, 'get_project_name') else ""
        self.main_win.log_info(f"Generating feature '{name}' for project [{project_name}]...")
        
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        try:
            self.app_ctx.generate_feature_controller.execute(args, self.root_dir, project_name)
        except Exception as e:
            self.main_win.log_error(f"Execution crashed: {str(e)}")
        finally:
            sys.stdout = old_stdout
            
        output = new_stdout.getvalue()
        self.main_win.console.append_log(output)
        
        if "✅ Success" in output or "generated successfully" in output:
            self.main_win.log_success(f"Feature '{name}' generated successfully!")
            self.feature_name_input.clear()
        else:
            self.main_win.log_error("Generation failed. See console output.")

    def retranslate_ui(self, lang_code: str):
        self.name_label.setText(self.i18n_manager.translate("Feature Name (PascalCase, e.g. PlaceOrder)"))
        self.feature_name_input.setPlaceholderText(self.i18n_manager.translate("Feature Name (PascalCase, e.g. PlaceOrder)"))
        self.plat_label.setText(self.i18n_manager.translate("Select Target Platforms"))
        self.db_label.setText(self.i18n_manager.translate("Select Database Technology"))
        self.generate_btn.setText(self.i18n_manager.translate("🚀 Generate Feature"))
