from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from ..level_01_atoms.labels import HeaderLabel


class BasePageTemplate(QWidget):
    """
    Template cấp độ 4 (Templates) trong thiết kế Atomic UI.
    Định nghĩa cấu trúc layout chung cho tất cả các trang con.
    """

    def __init__(self, title_key: str, app_ctx, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.app_ctx = app_ctx
        self.theme_manager = app_ctx.theme_manager
        self.i18n_manager = app_ctx.i18n_manager
        self.title_key = title_key

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(24)

        self.header = HeaderLabel(self.i18n_manager.translate(self.title_key))
        self.main_layout.addWidget(self.header)

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(16)
        self.main_layout.addWidget(self.content_widget, stretch=1)

        self.i18n_manager.subscribe(self._handle_language_changed)

    def _handle_language_changed(self, lang_code: str):
        self.header.setText(self.i18n_manager.translate(self.title_key))
        self.retranslate_ui(lang_code)

    def retranslate_ui(self, lang_code: str):
        pass
