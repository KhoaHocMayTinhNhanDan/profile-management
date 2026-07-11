from ..abstract.i_buttons_product import AbstractButtons


class KivyButtons(AbstractButtons):
    def get_template(self) -> str:
        return """from kivy.uix.button import Button

class PrimaryButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.537, 0.706, 0.98, 1)  # #89b4fa
        self.font_size = '14sp'
        self.bold = True

class DangerButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.953, 0.545, 0.659, 1)  # #f38ba8
        self.font_size = '14sp'
        self.bold = True

class SecondaryButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.192, 0.196, 0.267, 1)  # #313244
        self.font_size = '14sp'
"""
