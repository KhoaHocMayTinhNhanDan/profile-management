import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget
from PyQt6.QtCore import QTimer

from scripts.util_dev.project_manager_app.layer_05_bootstrap.app_context_desktop import AppContextDesktop

from .theme import DARK_BG, SUCCESS_COLOR, ERROR_COLOR
from .level_02_molecules.console_log import LogConsole
from .level_03_organisms.sidebar import Sidebar

from .level_05_pages.generate_page import GeneratePage
from .level_05_pages.check_imports_page import CheckImportsPage
from .level_05_pages.saved_projects_page import SavedProjectsPage
from .level_05_pages.reset_workspace_page import ResetWorkspacePage

from scripts.util_dev.project_manager_app.config.project_config import read_project_name, write_project_name, clear_project_config


class MainWindow(QMainWindow):
    def __init__(self, root_dir):
        super().__init__()
        self.app_ctx = AppContextDesktop(root_dir)
        self.root_dir = root_dir
        
        # Áp dụng theme ban đầu
        self.app_ctx.theme_manager.apply_theme_to_app()
        self.app_ctx.i18n_manager.language_changed.connect(self._update_title)
        
        # Project-Centric: Đọc state dự án hiện tại
        self._project_name = read_project_name(root_dir)
        
        self.setWindowTitle("Clean Architecture Project Manager")
        self.resize(1000, 680)
        self.setMinimumSize(950, 620)
        
        # Central Widget & Base Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        base_layout = QHBoxLayout(central_widget)
        base_layout.setContentsMargins(0, 0, 0, 0)
        base_layout.setSpacing(0)
        
        # 1. SIDEBAR PANEL (Organism)
        self.sidebar_widget = Sidebar(root_dir, self.app_ctx.i18n_manager, self.switch_view)
        
        # 2. MAIN CONTENT AREA
        self.content_container = QWidget()
        self.content_container.setObjectName("content_container")
        main_content_layout = QVBoxLayout(self.content_container)
        main_content_layout.setContentsMargins(30, 25, 30, 25)
        main_content_layout.setSpacing(20)
        
        # Stacked views (Pages)
        self.views_stack = QStackedWidget()
        
        from .level_05_pages.dashboard_page import DashboardPage
        self.dashboard_page = DashboardPage(self, self.app_ctx, self.root_dir)
        self.generate_page = GeneratePage(self, self.app_ctx, self.root_dir)
        self.check_imports_page = CheckImportsPage(self, self.app_ctx, self.root_dir)
        self.saved_projects_page = SavedProjectsPage(self, self.app_ctx, self.root_dir)
        self.reset_workspace_page = ResetWorkspacePage(self, self.app_ctx)
        
        self.views_stack.addWidget(self.dashboard_page)      # index 0
        self.views_stack.addWidget(self.generate_page)       # index 1
        self.views_stack.addWidget(self.check_imports_page)  # index 2
        self.views_stack.addWidget(self.saved_projects_page) # index 3
        self.views_stack.addWidget(self.reset_workspace_page)# index 4
        
        main_content_layout.addWidget(self.views_stack, stretch=4)
        
        # 3. CONSOLE LOG PANEL (Molecule)
        self.console = LogConsole()
        main_content_layout.addWidget(self.console, stretch=1)
        
        # Assemble Window Layout
        base_layout.addWidget(self.sidebar_widget)
        base_layout.addWidget(self.content_container)
        
        self._update_title()
        self.log_info("System initialized. Welcome to Clean Architecture Project Manager.")
        
        # Project-Centric: Hiển thị welcome dialog nếu chưa có project
        # Project-Centric: Luôn đảm bảo bắt đầu ở Dashboard
        self.switch_view(0)

    def _update_title(self):
        if self._project_name:
            self.setWindowTitle(f"Clean Architecture Project Manager  —  📦 {self._project_name}")
        else:
            no_active = self.app_ctx.i18n_manager.translate("None")
            self.setWindowTitle(f"Clean Architecture Project Manager  —  [{no_active}]")

    def get_project_name(self) -> str:
        return self._project_name

    def set_project_name(self, name: str):
        self._project_name = name
        write_project_name(self.root_dir, name)
        self._update_title()
        self.dashboard_page.refresh_dashboard()

    def on_workspace_reset(self):
        """Được gọi sau khi Reset Workspace - xóa project config và quay về dashboard empty state."""
        clear_project_config(self.root_dir)
        self._project_name = ""
        self._update_title()
        self.dashboard_page.refresh_dashboard()
        self.switch_view(0)

    def switch_view(self, index):
        self.sidebar_widget.select_button(index)
        self.views_stack.setCurrentIndex(index)
        
        # Refresh views that list data
        if index == 0:
            self.dashboard_page.refresh_dashboard()
        elif index == 3:
            self.saved_projects_page.refresh_project_list()

    def log_info(self, text):
        self.console.append_log(f"[INFO] {text}")
        
    def log_success(self, text):
        self.console.append_log(f"<font color='{SUCCESS_COLOR}'>[SUCCESS] {text}</font>")
        
    def log_error(self, text):
        self.console.append_log(f"<font color='{ERROR_COLOR}'>[ERROR] {text}</font>")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../")))
    window.show()
    sys.exit(app.exec())
