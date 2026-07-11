from ..abstract.i_page_product import AbstractPage


class KivyPage(AbstractPage):
    def get_template(self, pascal_name: str, snake_name: str) -> str:
        return f"""from kivy.uix.boxlayout import BoxLayout
from src.shared.logger.app_logger import get_logger

logger = get_logger(__name__)

class {pascal_name}Page(BoxLayout):
    def __init__(self, context, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.context = context
        
        # Xây dựng giao diện trang con Kivy tại đây
        # Ví dụ:
        # from ..level_01_atoms.labels import HeaderLabel
        # self.add_widget(HeaderLabel(text="Trang {pascal_name} đã sẵn sàng."))

# =========================================================================
# 🛠️ MOBILE UI INSPECTOR (GUIDELINE FOR MOBILE DEVELOPERS)
# Nhấn giữ chuột phải (hoặc chạm nhiều ngón) để in thông tin phân cấp widget Kivy:
# Để kích hoạt, thừa kế hoặc gọi phương thức gỡ lỗi dưới đây trong Main Window/App:
#
# class MobileUIInspectorBehavior:
#     def on_touch_down(self, touch):
#         if 'button' in touch.profile and touch.button == 'right':
#             # Quét phần tử dưới tọa độ điểm chạm
#             for child in self.walk():
#                 if child.collide_point(*touch.pos):
#                     print(f"[UI Inspector Mobile] Class: {{child.__class__.__name__}}, Size: {{child.size}}")
#         return super().on_touch_down(touch)
# =========================================================================
"""
