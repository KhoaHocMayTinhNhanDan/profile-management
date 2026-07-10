import sys
from typing import Any
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QStackedWidget,
    QListWidgetItem, QLabel, QFrame
)
from PyQt6.QtCore import Qt
from .level_05_pages.welcome_page import WelcomePage
from .level_05_pages.create_profile_page import CreateProfilePage
from .level_05_pages.create_profile_template_page import CreateProfileTemplatePage
from .level_05_pages.document_manager_page import DocumentManagerPage

class MainWindow(QMainWindow):
    def __init__(self, context: Any = None):
        super().__init__()
        self.context = context
        self.theme_manager = context.theme_manager if context is not None else None
        self.i18n_manager = context.i18n_manager if context is not None else None
        self.mode_manager = context.mode_manager if context is not None else None
        
        self.setWindowTitle("Chương Trình Quản Lý Hồ Sơ Đơn Vị")
        self.resize(1024, 768)
        self.setMinimumSize(800, 600)
        
        # Status Bar
        sb = self.statusBar()
        if sb is not None:
            sb.showMessage("Hệ thống sẵn sàng.")
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main layout (Horizontal: Sidebar on left, content on right)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar Frame
        sidebar_frame = QFrame()
        sidebar_frame.setFixedWidth(200)
        sidebar_frame.setStyleSheet("background-color: #1e1e24; border-right: 1px solid #2d2d34;")
        sidebar_layout = QVBoxLayout(sidebar_frame)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(15)
        
        # App Title in Sidebar
        title_lbl = QLabel("HỒ SƠ ĐƠN VỊ")
        title_lbl.setStyleSheet("color: #ffffff; font-size: 16px; font-weight: bold; padding: 5px;")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(title_lbl)
        
        # Divider line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #2d2d34;")
        sidebar_layout.addWidget(line)
        
        # Navigation List
        self.nav_list = QListWidget()
        self.nav_list.setCursor(Qt.CursorShape.PointingHandCursor)
        self.nav_list.setStyleSheet("""
            QListWidget {
                border: none;
                background-color: transparent;
            }
            QListWidget::item {
                color: #a0a0a5;
                padding: 10px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QListWidget::item:hover {
                background-color: #2b2b36;
                color: #ffffff;
            }
            QListWidget::item:selected {
                background-color: #2a82da;
                color: #ffffff;
            }
        """)
        
        item_welcome = QListWidgetItem("📊 Dashboard")
        item_welcome.setData(Qt.ItemDataRole.UserRole, "welcome")
        
        item_create_profile = QListWidgetItem("📝 Tạo Hồ Sơ Mới")
        item_create_profile.setData(Qt.ItemDataRole.UserRole, "create_profile")
        
        item_create_template = QListWidgetItem("⚙️ Tạo Mẫu Hồ Sơ")
        item_create_template.setData(Qt.ItemDataRole.UserRole, "create_profile_template")
        
        self.nav_list.addItem(item_welcome)
        self.nav_list.addItem(item_create_profile)
        self.nav_list.addItem(item_create_template)
        sidebar_layout.addWidget(self.nav_list)
        sidebar_layout.addStretch()
        
        main_layout.addWidget(sidebar_frame)
        
        # Right Stacked Widget for pages
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: #121214; padding: 20px;")
        
        # Pages mapping
        self.pages_map = {
            "welcome": WelcomePage(self.context),
            "create_profile": CreateProfilePage(self.context),
            "create_profile_template": CreateProfileTemplatePage(self.context),
            "document_manager": DocumentManagerPage(self.context),
        }
        
        # Add pages to stacked widget
        for page_name, page_widget in self.pages_map.items():
            self.stacked_widget.addWidget(page_widget)
            
        main_layout.addWidget(self.stacked_widget, stretch=1)
        
        # Connect Navigation selection
        self.nav_list.itemClicked.connect(self._on_nav_item_clicked)
        
        # Set default page
        self.nav_list.setCurrentRow(0)
        self.switch_page("welcome")
        
        # Theme subscription
        if self.theme_manager is not None:
            self.theme_manager.subscribe(self.apply_theme_stylesheet)
        
        # UI Inspector (F12) for Debug Mode
        from .level_02_molecules.ui_inspector import UIInspector
        from PyQt6.QtGui import QShortcut, QKeySequence
        self.inspector = UIInspector(self)
        self.shortcut_inspect = QShortcut(QKeySequence("F12"), self)
        self.shortcut_inspect.activated.connect(self.toggle_inspector)

    def _on_nav_item_clicked(self, item):
        page_name = item.data(Qt.ItemDataRole.UserRole)
        if page_name:
            self.switch_page(page_name)

    def switch_page(self, page_name: str):
        if page_name in self.pages_map:
            page_widget = self.pages_map[page_name]
            self.stacked_widget.setCurrentWidget(page_widget)
            
            # Update sidebar selection highlight
            for i in range(self.nav_list.count()):
                item = self.nav_list.item(i)
                if item is not None and item.data(Qt.ItemDataRole.UserRole) == page_name:
                    self.nav_list.setCurrentItem(item)
                    break
            
            # Refresh welcome list data if switching to welcome
            if page_name == "welcome" and hasattr(page_widget, "refresh_data"):
                page_widget.refresh_data()
            # Refresh templates if switching to create_profile
            if page_name == "create_profile" and hasattr(page_widget, "refresh_templates"):
                page_widget.refresh_templates()

    def switch_to_document_manager(self, profile_id: str):
        page_widget = self.pages_map["document_manager"]
        page_widget.set_profile(profile_id)
        self.stacked_widget.setCurrentWidget(page_widget)
        # Deselect sidebar menu since document manager is a details page
        self.nav_list.clearSelection()

    def toggle_inspector(self):
        self.inspector.active = not self.inspector.active
        from PyQt6.QtWidgets import QApplication
        app = QApplication.instance()
        if not app:
            return
        if self.inspector.active:
            app.installEventFilter(self.inspector)
            print("[UI Inspector] BAT CHE DO DEBUG (F12) - Click vao bat ky widget nao de copy thong tin!")
        else:
            app.removeEventFilter(self.inspector)
            print("[UI Inspector] TAT CHE DO DEBUG.")

    def apply_theme_stylesheet(self, theme_name: str, qss: str):
        from PyQt6.QtWidgets import QApplication
        app = QApplication.instance()
        if isinstance(app, QApplication):
            app.setStyleSheet(qss)
