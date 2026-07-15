from ..abstract.i_labels_product import AbstractLabels


class KivyLabels(AbstractLabels):
    def get_template(self) -> str:
        return """from kivy.uix.label import Label

class HeaderLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = ({{ ACCENT_COLOR_KIVY_FLOAT }})  # {{ ACCENT_COLOR }}
        self.font_size = '{{ HEADER_FONT_SIZE }}'.replace('px', 'sp')
        self.bold = True

class BodyLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = ({{ TEXT_COLOR_KIVY_FLOAT }})  # {{ TEXT_COLOR }}
        self.font_size = '{{ BODY_FONT_SIZE }}'.replace('px', 'sp')
"""
