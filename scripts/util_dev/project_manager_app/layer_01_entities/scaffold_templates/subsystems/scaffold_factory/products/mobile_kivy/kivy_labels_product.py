from ..abstract.i_labels_product import AbstractLabels


class KivyLabels(AbstractLabels):
    def get_template(self) -> str:
        return """from kivy.uix.label import Label

class HeaderLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = (0.537, 0.706, 0.98, 1)  # #89b4fa
        self.font_size = '20sp'
        self.bold = True

class BodyLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = (0.804, 0.839, 0.957, 1)  # #cdd6f4
        self.font_size = '14sp'
"""
