from ..abstract.i_main_window_product import AbstractMainWindow


class Qt6MainWindow(AbstractMainWindow):
    """
    GoF Role: ConcreteProduct
    """

    def get_template(self, project_name: str = "Application") -> str:
        template = """import sys
import os
import importlib
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton, QStackedWidget
from PyQt6.QtCore import Qt, QPoint

class MainWindow(QMainWindow):
    def __init__(self, context=None):
        super().__init__()
        self.context = context
        self.theme_manager = context.theme_manager if context else None
        self.i18n_manager = context.i18n_manager if context else None
        self.mode_manager = context.mode_manager if context else None
        
        self.setWindowTitle("{project_name}")
        self.resize(1000, 700) # Increased default window size for sidebar layout
        
        # Central layout: Sidebar + Stacked Widget content area
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 1. Left Sidebar
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        sidebar_layout = QVBoxLayout(self.sidebar)
        
        # Calculate dynamic layouts based on theme tokens
        page_pad = 25
        sidebar_pad = 15
        spacing_val = 10
        if self.theme_manager:
            page_padding_str = self.theme_manager.get_token("PAGE_PADDING")
            page_pad = int(page_padding_str.replace("px", "")) if page_padding_str.endswith("px") else 25
            sidebar_pad = int(page_pad * 0.6)
            spacing_str = self.theme_manager.get_token("SPACING_BASE")
            spacing_val = int(spacing_str.replace("px", "")) if spacing_str.endswith("px") else 10
            
        sidebar_layout.setContentsMargins(sidebar_pad, page_pad, sidebar_pad, page_pad)
        sidebar_layout.setSpacing(spacing_val)
        
        # Sidebar Logo / Title
        sidebar_title = QLabel("{project_name}")
        sidebar_title.setObjectName("SidebarTitle")
        sidebar_layout.addWidget(sidebar_title)
        
        self.menu_buttons = {}
        
        # 2. Right Content Stack
        self.page_stack = QStackedWidget()
        
        # 3. Dynamic Page Discovery
        pages_dir = os.path.join(os.path.dirname(__file__), "level_05_pages")
        
        # Find all generated pages ending with _page.py
        page_modules = []
        if os.path.exists(pages_dir):
            for f in os.listdir(pages_dir):
                if f.endswith("_page.py") and f != "__init__.py":
                    page_modules.append(f[:-3])
        
        # Ensure welcome_page is always first
        page_modules.sort(key=lambda x: 0 if x == "welcome_page" else 1)
        
        for p_mod in page_modules:
            try:
                # Import module dynamically relative to package
                module = importlib.import_module(
                    f".level_05_pages.{p_mod}", 
                    package="src.layer_04_infrastructure.ui.desktop_qt6"
                )
                # Compute ClassName, e.g. welcome_page -> WelcomePage
                words = p_mod.split("_")
                class_name = "".join(w.capitalize() for w in words)
                
                if hasattr(module, class_name):
                    page_class = getattr(module, class_name)
                    page_inst = page_class(self.context)
                    
                    # Add to QStackedWidget
                    idx = self.page_stack.addWidget(page_inst)
                    
                    # Add Menu Button in Sidebar
                    if p_mod == "welcome_page":
                        display_name = "🏠 Welcome"
                    elif p_mod == "color_palette_demo_page":
                        display_name = "⚡ Palette Demo"
                    else:
                        clean_name = p_mod.replace("_page", "").replace("_", " ").title()
                        display_name = f"📦 {clean_name}"
                        
                    btn = QPushButton(display_name)
                    btn.clicked.connect(lambda checked, i=idx, b=btn: self.switch_page(i, b))
                    sidebar_layout.addWidget(btn)
                    self.menu_buttons[idx] = btn
                    
            except Exception as e:
                print(f"Error loading page module {p_mod}: {e}")
                
        sidebar_layout.addStretch()
        
        # Light/Dark mode toggle at sidebar bottom
        self.btn_mode_toggle = QPushButton("🌙 Theme")
        self.btn_mode_toggle.clicked.connect(self.toggle_mode)
        sidebar_layout.addWidget(self.btn_mode_toggle)
        
        main_layout.addWidget(self.sidebar, stretch=1)
        main_layout.addWidget(self.page_stack, stretch=4)
        
        # Subscribe to theme changes
        if self.theme_manager:
            self.theme_manager.subscribe(self.apply_theme_stylesheet)
            
        # Switch to first page by default
        if self.menu_buttons:
            first_idx = list(self.menu_buttons.keys())[0]
            self.switch_page(first_idx, self.menu_buttons[first_idx])
            
        # UI Inspector (F12) for Debug Mode (only loaded when config.DEBUG_UI is enabled)
        from src import config
        if getattr(config, "DEBUG_UI", True):
            from .level_02_molecules.ui_inspector import UIInspector
            from PyQt6.QtGui import QShortcut, QKeySequence
            self.inspector = UIInspector(self)
            
            self.shortcut_inspect = QShortcut(QKeySequence("F12"), self)
            self.shortcut_inspect.activated.connect(self.toggle_inspector)
            
            # F10: Widget Screenshot Mode (Continuous, saves to snapshots/)
            self.shortcut_screenshot_mode = QShortcut(QKeySequence("F10"), self)
            self.shortcut_screenshot_mode.activated.connect(self.toggle_screenshot_mode)
            
            # F9: Single Widget Screenshot Mode (Saves & overwrites widget_screenshot.png)
            self.shortcut_single_screenshot = QShortcut(QKeySequence("F9"), self)
            self.shortcut_single_screenshot.activated.connect(self.toggle_single_screenshot_mode)
            
            # Install filter immediately so F11 (screenshot) works out-of-the-box
            from PyQt6.QtWidgets import QApplication
            app = QApplication.instance()
            if app:
                app.installEventFilter(self.inspector)
        else:
            self.inspector = None

    def switch_page(self, index, button):
        self.page_stack.setCurrentIndex(index)
        for btn in self.menu_buttons.values():
            btn.setChecked(False)
        button.setChecked(True)

    def toggle_inspector(self):
        if not self.inspector:
            return
        self.inspector.active = not self.inspector.active
        self.inspector.screenshot_mode = False
        self.inspector.single_screenshot_mode = False
        if hasattr(self.inspector, "hover_overlay") and self.inspector.hover_overlay:
            self.inspector.hover_overlay.hide()
        if self.inspector.active:
            print("[UI Inspector] BAT CHE DO DEBUG (F12) - Ra chuot de hien vien, click de copy thong tin!")
        else:
            print("[UI Inspector] TAT CHE DO DEBUG.")
 
    def toggle_screenshot_mode(self):
        if not self.inspector:
            return
        self.inspector.screenshot_mode = not self.inspector.screenshot_mode
        self.inspector.single_screenshot_mode = False
        self.inspector.active = False
        if hasattr(self.inspector, "hover_overlay") and self.inspector.hover_overlay:
            self.inspector.hover_overlay.hide()
        if self.inspector.screenshot_mode:
            print("[UI Inspector] BAT CHE DO CHUP ANH PHAN TU (F10) - Ra chuot de chon, click de chup anh phan tu!")
        else:
            print("[UI Inspector] TAT CHE DO CHUP ANH PHAN TU.")

    def toggle_single_screenshot_mode(self):
        if not self.inspector:
            return
        self.inspector.single_screenshot_mode = not self.inspector.single_screenshot_mode
        self.inspector.screenshot_mode = False
        self.inspector.active = False
        if hasattr(self.inspector, "hover_overlay") and self.inspector.hover_overlay:
            self.inspector.hover_overlay.hide()
        if self.inspector.single_screenshot_mode:
            print("[UI Inspector] BAT CHE DO CHUP ANH DON (F9) - Ra chuot de chon, click de ghi de widget_screenshot.png!")
        else:
            print("[UI Inspector] TAT CHE DO CHUP ANH DON.")

    def toggle_mode(self):
        if self.mode_manager:
            current = self.mode_manager.get_current_mode()
            new_mode = "light" if current == "dark" else "dark"
            self.mode_manager.switch_mode(new_mode)

    def apply_theme_stylesheet(self, theme_name: str, qss: str):
        from PyQt6.QtWidgets import QApplication
        app = QApplication.instance()
        if isinstance(app, QApplication):
            app.setStyleSheet(qss)
            
        # Apply local styling to Sidebar elements
        tm = self.theme_manager
        if tm:
            dark_bg = tm.get_color("DARK_BG")
            sidebar_bg = tm.get_color("SIDEBAR_BG")
            text_color = tm.get_color("TEXT_COLOR")
            accent_color = tm.get_color("ACCENT_COLOR")
            border_color = tm.get_color("BORDER_COLOR")
            
            radius = tm.get_token("RADIUS")
            border_width = tm.get_token("BORDER_WIDTH")
            button_padding = tm.get_token("BUTTON_PADDING")
            button_font_size = tm.get_token("BUTTON_FONT_SIZE")
            input_padding = tm.get_token("INPUT_PADDING")
            status_font_size = tm.get_token("STATUS_FONT_SIZE")
            button_border_radius = tm.get_token("BUTTON_BORDER_RADIUS")
            button_min_width = tm.get_token("BUTTON_MIN_WIDTH")
            button_min_height = tm.get_token("BUTTON_MIN_HEIGHT")
            sidebar_width = tm.get_token("SIDEBAR_WIDTH")
            
            # Set fixed sidebar width dynamically
            sidebar_w_val = int(sidebar_width.replace("px", "")) if sidebar_width.endswith("px") else 220
            self.sidebar.setFixedWidth(sidebar_w_val)
            
            qss_sidebar = f'''
                QFrame#Sidebar {{
                    background-color: {sidebar_bg};
                    border-right: {border_width} solid {border_color};
                }}
                QLabel {{
                    color: {text_color};
                }}
                QLabel#SidebarTitle {{
                    font-weight: bold;
                    font-size: {tm.get_token("HEADER_FONT_SIZE")};
                    margin-bottom: {tm.get_token("LABEL_MARGIN_BOTTOM")};
                }}
            '''
            self.sidebar.setStyleSheet(qss_sidebar)
            
            qss_btn = f'''
                QPushButton {{
                    background-color: transparent;
                    color: {text_color};
                    border: none;
                    border-radius: {button_border_radius};
                    padding: {button_padding};
                    text-align: left;
                    font-size: {button_font_size};
                    font-weight: bold;
                    min-height: {button_min_height};
                }}
                QPushButton:hover {{
                    background-color: {dark_bg};
                }}
                QPushButton:checked {{
                    background-color: {accent_color};
                    color: {sidebar_bg};
                }}
            '''
            for btn in self.menu_buttons.values():
                btn.setStyleSheet(qss_btn)
                btn.setCheckable(True)
                
            self.btn_mode_toggle.setStyleSheet(f'''
                QPushButton {{
                    background-color: {dark_bg};
                    color: {text_color};
                    border: {border_width} solid {border_color};
                    border-radius: {button_border_radius};
                    padding: {input_padding};
                    font-size: {status_font_size};
                    font-weight: bold;
                    min-height: {button_min_height};
                }}
                QPushButton:hover {{
                    border-color: {accent_color};
                }}
            ''')
            
            is_dark = self.mode_manager.is_dark() if self.mode_manager else True
            self.btn_mode_toggle.setText("🌙 Dark" if is_dark else "☀️ Light")
"""
        return template.replace("{project_name}", project_name)
