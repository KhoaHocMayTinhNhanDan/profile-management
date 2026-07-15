from ..abstract.i_inputs_product import AbstractInputs


class KivyInputs(AbstractInputs):
    def get_template(self) -> str:
        return """from kivy.uix.textinput import TextInput

class FormTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = ({{ CARD_BG_KIVY_FLOAT }})  # {{ CARD_BG }}
        self.foreground_color = ({{ TEXT_COLOR_KIVY_FLOAT }})  # {{ TEXT_COLOR }}
        self.multiline = False
        
        # Parse CSS padding "top left" or "top right bottom left" to Kivy [left, top, right, bottom]
        raw_p = '{{ INPUT_PADDING }}'.replace('px', '').split()
        if len(raw_p) == 2:
            self.padding = [float(raw_p[1]), float(raw_p[0]), float(raw_p[1]), float(raw_p[0])]
        elif len(raw_p) == 4:
            self.padding = [float(raw_p[3]), float(raw_p[0]), float(raw_p[1]), float(raw_p[2])]
        else:
            self.padding = [10, 10, 10, 10]
"""
