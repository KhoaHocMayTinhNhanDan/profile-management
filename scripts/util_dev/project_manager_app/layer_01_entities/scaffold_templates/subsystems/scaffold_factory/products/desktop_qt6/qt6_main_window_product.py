from ..abstract.i_main_window_product import AbstractMainWindow


class Qt6MainWindow(AbstractMainWindow):
    def get_template(self) -> str:
        return """import sys
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from .level_05_pages.welcome_page import WelcomePage

class MainWindow(QMainWindow):
    def __init__(self, context=None):
        super().__init__()
        self.context = context
        self.theme_manager = context.theme_manager
        self.i18n_manager = context.i18n_manager
        self.mode_manager = context.mode_manager
        
        self.setWindowTitle("Application")
        self.resize(800, 600)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Add welcome page
        self.welcome_page = WelcomePage(self.context)
        layout.addWidget(self.welcome_page)
        
        # Apply theme stylesheet & subscribe
        self.theme_manager.subscribe(self.apply_theme_stylesheet)
        
        # UI Inspector (F12) for Debug Mode
        from .level_02_molecules.ui_inspector import UIInspector
        from PyQt6.QtGui import QShortcut, QKeySequence
        self.inspector = UIInspector(self)
        self.shortcut_inspect = QShortcut(QKeySequence("F12"), self)
        self.shortcut_inspect.activated.connect(self.toggle_inspector)

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
        if app:
            app.setStyleSheet(qss)
"""
