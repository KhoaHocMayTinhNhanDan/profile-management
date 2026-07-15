from ..abstract.i_buttons_product import AbstractButtons


class KivyButtons(AbstractButtons):
    def get_template(self) -> str:
        return """from kivy.uix.button import Button

class PrimaryButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = ({{ ACCENT_COLOR_KIVY_FLOAT }})  # {{ ACCENT_COLOR }}
        self.font_size = '{{ BUTTON_FONT_SIZE }}'.replace('px', 'sp')
        self.bold = True

class DangerButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = ({{ ERROR_COLOR_KIVY_FLOAT }})  # {{ ERROR_COLOR }}
        self.font_size = '{{ BUTTON_FONT_SIZE }}'.replace('px', 'sp')
        self.bold = True

class SecondaryButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = ({{ BORDER_COLOR_KIVY_FLOAT }})  # {{ BORDER_COLOR }}
        self.font_size = '{{ BUTTON_FONT_SIZE }}'.replace('px', 'sp')
"""
