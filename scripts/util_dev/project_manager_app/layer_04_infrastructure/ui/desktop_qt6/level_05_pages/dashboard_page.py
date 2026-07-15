import os
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ..level_01_atoms.labels import HeaderLabel, SubtitleLabel, BodyLabel
from ..level_01_atoms.inputs import FormLineEdit
from ..level_01_atoms.buttons import PrimaryButton, SecondaryButton
from scripts.util_dev.project_manager_app.config.project_config import (
    write_project_name,
)
from ..level_04_templates.page_template import BasePageTemplate


class DashboardPage(BasePageTemplate):
    """
    DashboardPage - Trang hiển thị tổng quan thông tin dự án.
    Không dùng setStyleSheet inline tĩnh để đảm bảo đồng bộ hóa theme động 100%.
    """

    def __init__(self, main_win, app_ctx, root_dir):
        super().__init__("Dashboard", app_ctx)
        self.main_win = main_win
        self.root_dir = root_dir

        # Stacked Widget to switch between "No Project" and "Active Project" views
        self.stack = QStackedWidget()
        self.content_layout.addWidget(self.stack)

        # Build views
        self._init_no_project_view()
        self._init_active_project_view()

        self.stack.addWidget(self.no_project_widget)  # index 0
        self.stack.addWidget(self.active_project_widget)  # index 1

        self.refresh_dashboard()

    def _init_no_project_view(self):
        self.no_project_widget = QWidget()
        layout = QVBoxLayout(self.no_project_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        self.lbl_desc = BodyLabel(
            "Workspace is currently empty. Please create a new project or restore a saved session below."
        )
        layout.addWidget(self.lbl_desc)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        # 1. New Project Card
        new_card = QFrame()
        new_card.setObjectName("new_project_card")
        new_layout = QVBoxLayout(new_card)
        new_layout.setContentsMargins(20, 20, 20, 20)
        new_layout.setSpacing(15)

        self.lbl_new_title = SubtitleLabel("✨ Create New Project")
        self.lbl_new_title.setObjectName("lbl_new_title")
        new_layout.addWidget(self.lbl_new_title)

        self.new_proj_input = FormLineEdit("Project name (e.g. trading_bot)")
        new_layout.addWidget(self.new_proj_input)

        self.btn_create = PrimaryButton("🚀 Create Project")
        self.btn_create.clicked.connect(self.handle_create_project)
        new_layout.addWidget(self.btn_create)
        new_layout.addStretch()

        cards_layout.addWidget(new_card, stretch=1)

        # 2. Load Project Card
        load_card = QFrame()
        load_card.setObjectName("load_project_card")
        load_layout = QVBoxLayout(load_card)
        load_layout.setContentsMargins(20, 20, 20, 20)
        load_layout.setSpacing(15)

        self.lbl_load_title = SubtitleLabel("📂 Saved Sessions")
        self.lbl_load_title.setObjectName("lbl_load_title")
        load_layout.addWidget(self.lbl_load_title)

        self.project_list = QListWidget()
        load_layout.addWidget(self.project_list)

        self.btn_load = SecondaryButton("📂 Restore Session")
        self.btn_load.clicked.connect(self.handle_load_project)
        load_layout.addWidget(self.btn_load)

        cards_layout.addWidget(load_card, stretch=1)

        layout.addLayout(cards_layout)
        layout.addStretch()

    def _init_active_project_view(self):
        self.active_project_widget = QWidget()
        layout = QVBoxLayout(self.active_project_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # Welcome Card (Project Status)
        status_card = QFrame()
        status_card.setObjectName("status_card")
        status_layout = QVBoxLayout(status_card)
        status_layout.setContentsMargins(25, 25, 25, 25)
        status_layout.setSpacing(10)

        self.project_name_label = QLabel()
        self.project_name_label.setFont(QFont("Inter", 16, QFont.Weight.Bold))
        self.project_name_label.setObjectName("project_name_label")

        self.project_stats_label = BodyLabel("Updating...")

        status_layout.addWidget(self.project_name_label)
        status_layout.addWidget(self.project_stats_label)
        layout.addWidget(status_card)

        # Quick Actions
        self.lbl_actions = SubtitleLabel("Quick Actions")
        layout.addWidget(self.lbl_actions)

        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(15)

        self.btn_add_feat = PrimaryButton("➕ Add Feature")
        self.btn_add_feat.clicked.connect(lambda: self.main_win.switch_view(1))

        self.btn_check_arch = SecondaryButton("🛡️ Check Architecture")
        self.btn_check_arch.clicked.connect(lambda: self.main_win.switch_view(2))

        self.btn_backups = SecondaryButton("💾 View Backups")
        self.btn_backups.clicked.connect(lambda: self.main_win.switch_view(3))

        actions_layout.addWidget(self.btn_add_feat)
        actions_layout.addWidget(self.btn_check_arch)
        actions_layout.addWidget(self.btn_backups)
        actions_layout.addStretch()
        layout.addLayout(actions_layout)

        # Features List
        self.lbl_feats = SubtitleLabel("Generated Features (Use Cases)")
        layout.addWidget(self.lbl_feats)

        self.features_list = QListWidget()
        layout.addWidget(self.features_list)
        layout.addStretch()

    def handle_create_project(self):
        name = self.new_proj_input.text().strip()
        if not name:
            self.main_win.log_error("Project name cannot be empty!")
            return

        self.main_win.log_info(
            f"Scaffolding directory structure and UI skeleton for project [{name}]..."
        )

        from scripts.util_dev.project_manager_app.layer_02_usecases.usecases.generate_feature.generate_feature_dto import (
            GenerateFeatureInput,
        )

        input_data = GenerateFeatureInput(
            feature_name="",
            platforms=["desktop_qt6", "web_fastapi"],
            db_techs=["sqlite"],
            project_root_dir=self.root_dir,
            project_name=name,
        )

        output = self.app_ctx.generate_feature_interactor.execute(input_data)

        if output.status == "ok":
            if write_project_name(self.root_dir, name):
                self.main_win.set_project_name(name)
                self.main_win.log_success(
                    f"Project [{name}] created and activated successfully!"
                )
                self.new_proj_input.clear()
                self.refresh_dashboard()
            else:
                self.main_win.log_error("Failed to save project configuration!")
        else:
            self.main_win.log_error(f"Scaffolding failed: {output.message}")

    def handle_load_project(self):
        selected = self.project_list.currentItem()
        if not selected or not selected.flags() & Qt.ItemFlag.ItemIsSelectable:
            self.main_win.log_error("Please select a project from the list!")
            return
        text = selected.text()
        src_dir = os.path.join(self.root_dir, "src")
        tests_dir = os.path.join(self.root_dir, "tests")
        ok = self.app_ctx.load_controller.execute(text, src_dir, tests_dir)
        if ok:
            self.main_win.set_project_name(text)
            self.main_win.log_success(f"Loaded and activated project: [{text}]")
            self.refresh_dashboard()
        else:
            self.main_win.log_error(f"Failed to load project '{text}'!")

    def _load_saved_projects(self):
        self.project_list.clear()
        try:
            projs = self.app_ctx.list_controller.execute()
            if not projs:
                item = QListWidgetItem("(No saved projects found)")
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
                item.setForeground(Qt.GlobalColor.gray)
                self.project_list.addItem(item)
            else:
                for p in projs:
                    self.project_list.addItem(p)
        except Exception:
            pass

    def refresh_dashboard(self):
        project_name = (
            self.main_win.get_project_name()
            if hasattr(self.main_win, "get_project_name")
            else ""
        )
        if not project_name:
            self.stack.setCurrentIndex(0)
            self._load_saved_projects()
            return

        self.stack.setCurrentIndex(1)
        self.project_name_label.setText(f"📦 {project_name}")

        # Scan src/layer_02_usecases/usecases for features
        usecases_dir = os.path.join(
            self.root_dir, "src", "layer_02_usecases", "usecases"
        )
        features = []
        if os.path.exists(usecases_dir):
            for item in os.listdir(usecases_dir):
                if item != "__pycache__" and os.path.isdir(
                    os.path.join(usecases_dir, item)
                ):
                    features.append(item)

        self.features_list.clear()
        if not features:
            item = QListWidgetItem(
                self.i18n_manager.translate("No features have been created yet.")
            )
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            item.setForeground(Qt.GlobalColor.gray)
            self.features_list.addItem(item)
            self.project_stats_label.setText(
                self.i18n_manager.translate("Project is currently empty.")
            )
        else:
            for feat in sorted(features):
                self.features_list.addItem(f"✨ {feat}")
            self.project_stats_label.setText(
                self.i18n_manager.translate(
                    "Project has {count} feature(s) scaffolded.", count=len(features)
                )
            )

    def retranslate_ui(self, lang_code: str):
        self.lbl_desc.setText(
            self.i18n_manager.translate(
                "Workspace is currently empty. Please create a new project or restore a saved session below."
            )
        )
        self.lbl_new_title.setText(self.i18n_manager.translate("✨ Create New Project"))
        self.new_proj_input.setPlaceholderText(
            self.i18n_manager.translate("Project name (e.g. trading_bot)")
        )
        self.btn_create.setText(self.i18n_manager.translate("🚀 Create Project"))
        self.lbl_load_title.setText(self.i18n_manager.translate("📂 Saved Sessions"))
        self.btn_load.setText(self.i18n_manager.translate("📂 Restore Session"))
        self.lbl_actions.setText(self.i18n_manager.translate("Quick Actions"))
        self.btn_add_feat.setText(self.i18n_manager.translate("➕ Add Feature"))
        self.btn_check_arch.setText(
            self.i18n_manager.translate("🛡️ Check Architecture")
        )
        self.btn_backups.setText(self.i18n_manager.translate("💾 View Backups"))
        self.lbl_feats.setText(
            self.i18n_manager.translate("Generated Features (Use Cases)")
        )
        self.refresh_dashboard()
