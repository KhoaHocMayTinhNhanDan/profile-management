from typing import Any
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QListWidget,
    QStackedWidget,
    QListWidgetItem,
    QLabel,
    QFrame,
    QMessageBox,
    QComboBox,
    QProgressBar,
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

        # Menu Bar
        menu_bar = self.menuBar()
        if menu_bar is not None:
            file_menu = menu_bar.addMenu("Hệ thống")
            if file_menu is not None:
                exit_action = QAction("Thoát", self)
                exit_action.setShortcut("Ctrl+Q")
                exit_action.triggered.connect(self.close)
                file_menu.addAction(exit_action)

            help_menu = menu_bar.addMenu("Trợ giúp")
            if help_menu is not None:
                about_action = QAction("Giới thiệu", self)
                about_action.triggered.connect(self._show_about_dialog)
                help_menu.addAction(about_action)

        # Centralized Status Bar Configuration (Change alignment in one place: "left" or "right")
        self.STATUS_ALIGNMENT = "right"  # Can be "left" or "right"

        # Styled loading widget for status bar (including a pulsing indeterminate QProgressBar)
        self.status_loading_widget = QFrame()
        self.status_loading_widget.setObjectName("status_loading_container")
        self.status_loading_widget.setStyleSheet(
            "background: transparent; border: none;"
        )

        status_layout = QHBoxLayout(self.status_loading_widget)
        status_layout.setContentsMargins(5, 0, 5, 0)
        status_layout.setSpacing(10)

        self.status_loading_label = QLabel("Đang xử lý, vui lòng chờ...")
        self.status_loading_label.setStyleSheet(
            "color: #cdd6f4; font-size: 13px; font-weight: bold;"
        )

        self.status_progress_bar = QProgressBar()
        self.status_progress_bar.setRange(0, 0)  # Pulse animation
        self.status_progress_bar.setTextVisible(False)
        self.status_progress_bar.setFixedHeight(12)
        self.status_progress_bar.setFixedWidth(120)
        self.status_progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid rgba(137, 180, 250, 0.4);
                border-radius: 6px;
                background-color: rgba(30, 41, 59, 0.6);
            }
            QProgressBar::chunk {
                background-color: #89b4fa;
                border-radius: 5px;
            }
        """)

        # Add stretch to push text and progress bar close to each other on the right
        status_layout.addStretch(1)
        status_layout.addWidget(self.status_loading_label)
        status_layout.addWidget(self.status_progress_bar)

        # Styled message label for permanent status notifications (right-aligned)
        self.status_msg_label = QLabel()
        self.status_msg_label.setStyleSheet(
            "color: #cdd6f4; font-size: 13px; font-weight: bold; background: transparent;"
        )

        sb = self.statusBar()
        if sb is not None:
            self.show_status_message("Hệ thống sẵn sàng.", "ready", 0)

        # Central widget
        central = QWidget()
        central.setObjectName("content_container")
        self.setCentralWidget(central)

        # Main layout (Horizontal: Sidebar on left, content on right)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar Frame
        sidebar_frame = QFrame()
        sidebar_frame.setObjectName("sidebar")
        sidebar_frame.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar_frame)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(15)

        # App Title in Sidebar
        title_lbl = QLabel("HỒ SƠ ĐƠN VỊ")
        title_lbl.setObjectName("sidebar_title")
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(title_lbl)

        # Divider line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setObjectName("sidebar_divider")
        sidebar_layout.addWidget(line)

        # Navigation List
        self.nav_list = QListWidget()
        self.nav_list.setCursor(Qt.CursorShape.PointingHandCursor)

        welcome_txt = (
            self.i18n_manager.translate("welcome") if self.i18n_manager else "Dashboard"
        )
        create_profile_txt = (
            self.i18n_manager.translate("create_profile")
            if self.i18n_manager
            else "Create New Profile"
        )
        create_template_txt = (
            self.i18n_manager.translate("create_profile_template")
            if self.i18n_manager
            else "Create Profile Template"
        )

        item_welcome = QListWidgetItem("📊 " + welcome_txt)
        item_welcome.setData(Qt.ItemDataRole.UserRole, "welcome")

        item_create_profile = QListWidgetItem("📝 " + create_profile_txt)
        item_create_profile.setData(Qt.ItemDataRole.UserRole, "create_profile")

        item_create_template = QListWidgetItem("⚙️ " + create_template_txt)
        item_create_template.setData(
            Qt.ItemDataRole.UserRole, "create_profile_template"
        )

        self.nav_list.addItem(item_welcome)
        self.nav_list.addItem(item_create_profile)
        self.nav_list.addItem(item_create_template)
        sidebar_layout.addWidget(self.nav_list)
        sidebar_layout.addStretch()

        # Settings Container at the bottom of Sidebar
        self.settings_frame = QFrame()
        self.settings_frame.setObjectName("settings_container")
        settings_layout = QVBoxLayout(self.settings_frame)
        settings_layout.setContentsMargins(6, 6, 6, 6)
        settings_layout.setSpacing(4)

        # Language Selector
        self.lbl_lang = QLabel(
            self.i18n_manager.translate("language")
            if self.i18n_manager
            else "Ngôn ngữ:"
        )
        self.lbl_lang.setObjectName("settings_label")
        self.combo_lang = QComboBox()
        self.combo_lang.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_layout.addWidget(self.lbl_lang)
        settings_layout.addWidget(self.combo_lang)

        # Theme Selector
        self.lbl_theme = QLabel(
            self.i18n_manager.translate("theme") if self.i18n_manager else "Chủ đề:"
        )
        self.lbl_theme.setObjectName("settings_label")
        self.combo_theme = QComboBox()
        self.combo_theme.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_layout.addWidget(self.lbl_theme)
        settings_layout.addWidget(self.combo_theme)

        # Mode Selector
        self.lbl_mode = QLabel(
            self.i18n_manager.translate("mode") if self.i18n_manager else "Chế độ:"
        )
        self.lbl_mode.setObjectName("settings_label")
        self.combo_mode = QComboBox()
        self.combo_mode.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_layout.addWidget(self.lbl_mode)
        settings_layout.addWidget(self.combo_mode)

        sidebar_layout.addWidget(self.settings_frame)

        # Populate settings
        self._populate_settings()

        main_layout.addWidget(sidebar_frame)

        # Right Stacked Widget for pages
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setObjectName("main_stack")

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

        # Theme & i18n subscription
        if self.theme_manager is not None:
            self.theme_manager.subscribe(self.apply_theme_stylesheet)
        if self.i18n_manager is not None:
            self.i18n_manager.subscribe(self._handle_language_changed)

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
                if (
                    item is not None
                    and item.data(Qt.ItemDataRole.UserRole) == page_name
                ):
                    self.nav_list.setCurrentItem(item)
                    break

            # Refresh welcome list data if switching to welcome
            if page_name == "welcome" and hasattr(page_widget, "refresh_data"):
                page_widget.refresh_data()
            # Refresh templates if switching to create_profile
            if page_name == "create_profile" and hasattr(
                page_widget, "refresh_templates"
            ):
                page_widget.refresh_templates()
            # Reset edit mode when switching to create_profile_template from nav menu
            if page_name == "create_profile_template" and hasattr(
                page_widget, "set_template_id_for_editing"
            ):
                page_widget.set_template_id_for_editing(None)

    def switch_to_document_manager(self, profile_id: str):
        page_widget = self.pages_map["document_manager"]
        page_widget.set_profile(profile_id)
        self.stacked_widget.setCurrentWidget(page_widget)
        # Deselect sidebar menu since document manager is a details page
        self.nav_list.clearSelection()

    def switch_to_edit_template(self, template_id: str):
        page_widget = self.pages_map["create_profile_template"]
        if hasattr(page_widget, "set_template_id_for_editing"):
            page_widget.set_template_id_for_editing(template_id)
        self.stacked_widget.setCurrentWidget(page_widget)
        # Deselect sidebar menu since this is a details/edit page
        self.nav_list.clearSelection()

    def toggle_inspector(self):
        self.inspector.active = not self.inspector.active
        from PyQt6.QtWidgets import QApplication

        app = QApplication.instance()
        if not app:
            return
        if self.inspector.active:
            app.installEventFilter(self.inspector)
            print(
                "[UI Inspector] BAT CHE DO DEBUG (F12) - Click vao bat ky widget nao de copy thong tin!"
            )
        else:
            app.removeEventFilter(self.inspector)
            print("[UI Inspector] TAT CHE DO DEBUG.")

    def apply_theme_stylesheet(self, theme_name: str, qss: str):
        from PyQt6.QtWidgets import QApplication

        app = QApplication.instance()
        if isinstance(app, QApplication):
            app.setStyleSheet(qss)

    def _show_about_dialog(self):
        QMessageBox.about(
            self,
            "Giới thiệu",
            "<h3>Chương Trình Quản Lý Hồ Sơ Đơn Vị</h3>"
            "<p>Hệ thống quản trị hồ sơ và tài liệu đơn vị tự động theo Kiến trúc Sạch (Clean Architecture).</p>"
            "<p>Phiên bản: 1.0.0</p>",
        )

    def _populate_settings(self):
        # Populate Languages
        if self.i18n_manager:
            available_langs = self.i18n_manager.get_available_languages()
            for code, name in available_langs.items():
                self.combo_lang.addItem(name, code)

            current_lang = self.i18n_manager.get_current_lang()
            index = self.combo_lang.findData(current_lang)
            if index >= 0:
                self.combo_lang.setCurrentIndex(index)
            self.combo_lang.currentIndexChanged.connect(self._on_language_changed)

        # Populate Themes
        if self.theme_manager:
            themes = self.theme_manager.get_available_themes()
            for theme_name in themes:
                self.combo_theme.addItem(theme_name.capitalize(), theme_name)
            current_theme = self.theme_manager.get_current_theme()
            index = self.combo_theme.findData(current_theme)
            if index >= 0:
                self.combo_theme.setCurrentIndex(index)
            self.combo_theme.currentIndexChanged.connect(self._on_theme_changed)

        # Populate Modes
        if self.mode_manager:
            self.combo_mode.addItem("Tối / Dark", "dark")
            self.combo_mode.addItem("Sáng / Light", "light")
            current_mode = self.mode_manager.get_current_mode()
            index = self.combo_mode.findData(current_mode)
            if index >= 0:
                self.combo_mode.setCurrentIndex(index)
            self.combo_mode.currentIndexChanged.connect(self._on_mode_changed)

    def _on_language_changed(self, index):
        if self.i18n_manager:
            lang_code = self.combo_lang.itemData(index)
            if lang_code:
                self.i18n_manager.switch_language(lang_code)

    def _on_theme_changed(self, index):
        if self.theme_manager:
            theme_name = self.combo_theme.itemData(index)
            if theme_name:
                self.theme_manager.switch_theme(theme_name)

    def _on_mode_changed(self, index):
        if self.mode_manager:
            mode_name = self.combo_mode.itemData(index)
            if mode_name:
                self.mode_manager.switch_mode(mode_name)

    def _handle_language_changed(self, lang_code: str):
        self.retranslate_ui(lang_code)

    def retranslate_ui(self, lang_code: str):
        if self.i18n_manager is None:
            return

        # Update navigation list items
        item_0 = self.nav_list.item(0)
        if item_0 is not None:
            item_0.setText("📊 " + self.i18n_manager.translate("welcome"))

        item_1 = self.nav_list.item(1)
        if item_1 is not None:
            item_1.setText("📝 " + self.i18n_manager.translate("create_profile"))

        item_2 = self.nav_list.item(2)
        if item_2 is not None:
            item_2.setText(
                "⚙️ " + self.i18n_manager.translate("create_profile_template")
            )

        # Update settings labels
        if hasattr(self, "lbl_lang"):
            self.lbl_lang.setText(self.i18n_manager.translate("language") + ":")
        if hasattr(self, "lbl_theme"):
            self.lbl_theme.setText(self.i18n_manager.translate("theme") + ":")
        if hasattr(self, "lbl_mode"):
            self.lbl_mode.setText(self.i18n_manager.translate("mode") + ":")

        # Update status bar message
        sb = self.statusBar()
        if sb is not None:
            self.show_status_message(
                self.i18n_manager.translate("status_ready") or "Ready.",
                "ready",
                0,
            )

    def _add_status_widget(self, widget):
        sb = self.statusBar()
        if sb is not None:
            if self.STATUS_ALIGNMENT == "right":
                sb.addPermanentWidget(widget)
            else:
                sb.addWidget(widget)

    def _remove_status_widget(self, widget):
        sb = self.statusBar()
        if sb is not None:
            sb.removeWidget(widget)

    def set_loading(self, is_loading: bool):
        sb = self.statusBar()
        if sb is None:
            return

        if is_loading:
            # 1. Hide and remove any existing message label to avoid overlap
            self._clear_status_message()

            # 2. Show loading widget
            self._remove_status_widget(self.status_loading_widget)
            self._add_status_widget(self.status_loading_widget)
            self.status_loading_widget.show()
            sb.clearMessage()
        else:
            self.status_loading_widget.hide()
            self._remove_status_widget(self.status_loading_widget)

    def show_status_message(
        self, msg: str, status_type: str = "info", timeout_ms: int = 5000
    ):
        sb = self.statusBar()
        if sb is None:
            return

        # 1. Hide and remove loading widget to avoid overlap
        self.status_loading_widget.hide()
        self._remove_status_widget(self.status_loading_widget)

        # Determine color based on status_type
        colors = {
            "success": "#a6e3a1",  # soft green
            "error": "#f38ba8",  # soft red
            "info": "#89b4fa",  # soft blue
            "ready": "#cdd6f4",  # soft white/gray
        }
        color = colors.get(status_type, "#cdd6f4")

        self.status_msg_label.setStyleSheet(
            f"color: {color}; font-size: 13px; font-weight: bold; background: transparent; padding-right: 10px;"
        )
        self.status_msg_label.setText(msg)

        self._remove_status_widget(self.status_msg_label)
        self._add_status_widget(self.status_msg_label)
        self.status_msg_label.show()

        # Clear temporary text messages to avoid overlaps
        sb.clearMessage()

        if timeout_ms > 0:
            from PyQt6.QtCore import QTimer

            QTimer.singleShot(timeout_ms, self._restore_ready_status)

    def _clear_status_message(self):
        self.status_msg_label.hide()
        self._remove_status_widget(self.status_msg_label)

    def _restore_ready_status(self):
        # Only restore to "Hệ thống sẵn sàng" if we are not currently loading
        if not self.status_loading_widget.isVisible():
            self._clear_status_message()
            ready_txt = "Hệ thống sẵn sàng."
            if self.i18n_manager is not None:
                ready_txt = (
                    self.i18n_manager.translate("status_ready") or "Hệ thống sẵn sàng."
                )
            self.show_status_message(ready_txt, "ready", 0)
