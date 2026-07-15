from PyQt6.QtWidgets import QWidget, QVBoxLayout
from ...level_01_atoms import HeaderLabel


class BasePageTemplate(QWidget):
    """
    Template cấp độ 4 (Templates) trong thiết kế Atomic UI.
    Định nghĩa khung bố cục chung cho tất cả các trang:
      - Tự động tích hợp ThemeManager và I18nManager.
      - Cấu hình margins, spacing chuẩn.
      - Tự động sinh Header tiêu đề trang và hỗ trợ dịch tự động.
      - Cung cấp container `content_layout` cho các trang con tự điền nội dung.
    """

    def __init__(self, title_key: str, app_ctx, parent=None):
        super().__init__(parent)
        self.app_ctx = app_ctx
        self.theme_manager = app_ctx.theme_manager
        self.i18n_manager = app_ctx.i18n_manager
        self.title_key = title_key

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(20)

        # Header Tiêu đề chuẩn hóa hỗ trợ i18n
        self.header = HeaderLabel(self.i18n_manager.translate(self.title_key))
        self.main_layout.addWidget(self.header)

        # Container nội dung chính cho Page tự triển khai
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(15)
        self.main_layout.addWidget(self.content_widget, stretch=1)

        # Kết nối sự kiện thay đổi toàn cục
        self.i18n_manager.language_changed.connect(self._handle_language_changed)
        self.theme_manager.theme_changed.connect(self.update_theme_styles)

    def _handle_language_changed(self, lang_code: str):
        self.header.setText(self.i18n_manager.translate(self.title_key))
        self.retranslate_ui(lang_code)

    def retranslate_ui(self, lang_code: str):
        """Được ghi đè bởi các trang con để cập nhật ngôn ngữ cho các nhãn trong trang."""
        pass

    def update_theme_styles(self, theme_name: str):
        """Được ghi đè bởi các trang con để thay đổi phong cách hiển thị riêng (nếu cần)."""
        pass
