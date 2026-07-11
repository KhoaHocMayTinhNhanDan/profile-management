from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QLabel, QGridLayout
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from ..level_01_atoms.buttons import PrimaryButton
from ..level_04_templates.page_template import BasePageTemplate


class SetupEnvWorker(QThread):
    """
    Worker Thread để chạy setup môi trường ngầm không làm đơ giao diện PyQt6.
    """

    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    def run(self):
        def log_callback(msg: str):
            self.log_signal.emit(msg)

        res = self.controller.execute(log_callback=log_callback)
        self.finished_signal.emit(res.success, res.message)


class DeveloperUtilitiesPage(BasePageTemplate):
    """
    DeveloperUtilitiesPage - Trang tích hợp các tiện ích của nhà phát triển.
    Gồm: Check Architecture, Clean Code Migration, Setup Environment.
    Thiết kế 3 Cards sang trọng theo chuẩn UI/UX.
    """

    def __init__(self, main_win, app_ctx, root_dir):
        super().__init__("Developer Utilities", app_ctx)
        self.main_win = main_win
        self.root_dir = root_dir
        self.setup_worker = None

        # Main grid layout cho 3 cards
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)

        # ----------------------------------------------------
        # CARD 1: CHECK ARCHITECTURE
        # ----------------------------------------------------
        self.card_check = QFrame()
        self.card_check.setObjectName("utility_card")
        self.card_check.setProperty("class", "InteractiveCard")
        layout_check = QVBoxLayout(self.card_check)
        layout_check.setContentsMargins(20, 20, 20, 20)
        layout_check.setSpacing(10)

        self.lbl_check_icon = QLabel("🛡️")
        self.lbl_check_icon.setFont(QFont("Inter", 32))
        self.lbl_check_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_check_title = QLabel("Check Architecture")
        self.lbl_check_title.setFont(QFont("Inter", 12, QFont.Weight.Bold))
        self.lbl_check_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_check_title.setProperty("class", "HeaderLabel")

        self.lbl_check_desc = QLabel(
            "Scan project imports to enforce Clean Architecture layer rules."
        )
        self.lbl_check_desc.setFont(QFont("Inter", 9))
        self.lbl_check_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_check_desc.setWordWrap(True)
        self.lbl_check_desc.setProperty("class", "BodyLabel")

        self.btn_check = PrimaryButton("Scan Imports")
        self.btn_check.clicked.connect(self.handle_check_imports)

        layout_check.addWidget(self.lbl_check_icon)
        layout_check.addWidget(self.lbl_check_title)
        layout_check.addWidget(self.lbl_check_desc)
        layout_check.addStretch()
        layout_check.addWidget(self.btn_check)

        # ----------------------------------------------------
        # CARD 2: CLEAN CODE MIGRATION
        # ----------------------------------------------------
        self.card_migrate = QFrame()
        self.card_migrate.setObjectName("utility_card")
        self.card_migrate.setProperty("class", "InteractiveCard")
        layout_migrate = QVBoxLayout(self.card_migrate)
        layout_migrate.setContentsMargins(20, 20, 20, 20)
        layout_migrate.setSpacing(10)

        self.lbl_migrate_icon = QLabel("🪄")
        self.lbl_migrate_icon.setFont(QFont("Inter", 32))
        self.lbl_migrate_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_migrate_title = QLabel("Code Migration")
        self.lbl_migrate_title.setFont(QFont("Inter", 12, QFont.Weight.Bold))
        self.lbl_migrate_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_migrate_title.setProperty("class", "HeaderLabel")

        self.lbl_migrate_desc = QLabel(
            "Migrate Protocols to ABCs and replace print() statements with loggers."
        )
        self.lbl_migrate_desc.setFont(QFont("Inter", 9))
        self.lbl_migrate_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_migrate_desc.setWordWrap(True)
        self.lbl_migrate_desc.setProperty("class", "BodyLabel")

        self.btn_migrate = PrimaryButton("Run Migration")
        self.btn_migrate.clicked.connect(self.handle_migration)

        layout_migrate.addWidget(self.lbl_migrate_icon)
        layout_migrate.addWidget(self.lbl_migrate_title)
        layout_migrate.addWidget(self.lbl_migrate_desc)
        layout_migrate.addStretch()
        layout_migrate.addWidget(self.btn_migrate)

        # ----------------------------------------------------
        # CARD 3: SETUP ENVIRONMENT
        # ----------------------------------------------------
        self.card_setup = QFrame()
        self.card_setup.setObjectName("utility_card")
        self.card_setup.setProperty("class", "InteractiveCard")
        layout_setup = QVBoxLayout(self.card_setup)
        layout_setup.setContentsMargins(20, 20, 20, 20)
        layout_setup.setSpacing(10)

        self.lbl_setup_icon = QLabel("🛠️")
        self.lbl_setup_icon.setFont(QFont("Inter", 32))
        self.lbl_setup_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_setup_title = QLabel("Setup Environment")
        self.lbl_setup_title.setFont(QFont("Inter", 12, QFont.Weight.Bold))
        self.lbl_setup_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_setup_title.setProperty("class", "HeaderLabel")

        self.lbl_setup_desc = QLabel(
            "Initialize Python virtual environment (.venv) and install core libraries."
        )
        self.lbl_setup_desc.setFont(QFont("Inter", 9))
        self.lbl_setup_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_setup_desc.setWordWrap(True)
        self.lbl_setup_desc.setProperty("class", "BodyLabel")

        self.btn_setup = PrimaryButton("Setup Env")
        self.btn_setup.clicked.connect(self.handle_setup)

        layout_setup.addWidget(self.lbl_setup_icon)
        layout_setup.addWidget(self.lbl_setup_title)
        layout_setup.addWidget(self.lbl_setup_desc)
        layout_setup.addStretch()
        layout_setup.addWidget(self.btn_setup)

        # Add cards to Grid Layout (1 row, 3 columns)
        grid_layout.addWidget(self.card_check, 0, 0)
        grid_layout.addWidget(self.card_migrate, 0, 1)
        grid_layout.addWidget(self.card_setup, 0, 2)

        self.content_layout.addLayout(grid_layout)
        self.content_layout.addStretch()

    def handle_check_imports(self):
        self.main_win.log_info("Running static import dependency scan...")
        output = self.app_ctx.check_imports_controller.execute(self.root_dir)

        if output.status == "error":
            self.main_win.log_error("Architecture Rules Violated!")
            for v in output.violations or []:
                self.main_win.log_error(
                    f"Violation: {v[0]} (Layer {v[1]} imports Layer {v[2]})"
                )
        else:
            self.main_win.log_success(
                "Import dependency scan: All layer boundaries are clean."
            )

    def handle_migration(self):
        self.main_win.log_info(
            "Starting Protocol -> ABC and print -> logger code migration..."
        )
        res = self.app_ctx.migrate_clean_code_controller.execute(self.root_dir)
        self.main_win.log_success(res.message)
        if res.changed_interfaces:
            self.main_win.log_success("Updated interfaces:")
            for f in res.changed_interfaces:
                self.main_win.log_success(f"  ✅ {f}")
        if res.changed_prints:
            self.main_win.log_success("Replaced prints in:")
            for f in res.changed_prints:
                self.main_win.log_success(f"  ✅ {f}")

    def handle_setup(self):
        self.main_win.log_info(
            "Setting up Python virtual environment and core packages..."
        )
        self.btn_setup.setEnabled(False)
        self.btn_setup.setText("Setting up...")

        # Khởi chạy thread worker phụ
        self.setup_worker = SetupEnvWorker(self.app_ctx.setup_environment_controller)
        self.setup_worker.log_signal.connect(self.main_win.log_info)
        self.setup_worker.finished_signal.connect(self.on_setup_finished)
        self.setup_worker.start()

    def on_setup_finished(self, success: bool, message: str):
        self.btn_setup.setEnabled(True)
        self.btn_setup.setText(self.i18n_manager.translate("Setup Env"))
        if success:
            self.main_win.log_success(message)
        else:
            self.main_win.log_error(message)

    def retranslate_ui(self, lang_code: str):
        self.lbl_check_title.setText(self.i18n_manager.translate("Check Architecture"))
        self.lbl_check_desc.setText(
            self.i18n_manager.translate(
                "Scan project imports to enforce Clean Architecture layer rules."
            )
        )
        self.btn_check.setText(self.i18n_manager.translate("Scan Imports"))

        self.lbl_migrate_title.setText(self.i18n_manager.translate("Code Migration"))
        self.lbl_migrate_desc.setText(
            self.i18n_manager.translate(
                "Migrate Protocols to ABCs and replace print() statements with loggers."
            )
        )
        self.btn_migrate.setText(self.i18n_manager.translate("Run Migration"))

        self.lbl_setup_title.setText(self.i18n_manager.translate("Setup Environment"))
        self.lbl_setup_desc.setText(
            self.i18n_manager.translate(
                "Initialize Python virtual environment (.venv) and install core libraries."
            )
        )
        self.btn_setup.setText(self.i18n_manager.translate("Setup Env"))
