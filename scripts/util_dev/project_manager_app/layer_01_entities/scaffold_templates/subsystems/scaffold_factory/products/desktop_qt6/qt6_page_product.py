from ..abstract.i_page_product import AbstractPage


class Qt6Page(AbstractPage):
    def get_template(self, pascal_name: str, snake_name: str) -> str:
        return f"""from PyQt6.QtWidgets import QVBoxLayout
from src.shared.logger.app_logger import get_logger
from ..level_04_templates.page_template import BasePageTemplate

logger = get_logger(__name__)

class {pascal_name}Page(BasePageTemplate):
    def __init__(self, context):
        # Khởi tạo BasePageTemplate với tiêu đề và context
        super().__init__("{snake_name}", context)
        
        # Xây dựng giao diện trang con tại đây
        # Ví dụ:
        # from ..level_01_atoms.labels import BodyLabel
        # self.desc = BodyLabel("Trang {pascal_name} đã sẵn sàng.")
        # self.content_layout.addWidget(self.desc)
        
        self.content_layout.addStretch()

    def retranslate_ui(self, lang_code: str):
        # Cập nhật ngôn ngữ động cho các thành phần con tại đây nếu cần
        pass
"""
