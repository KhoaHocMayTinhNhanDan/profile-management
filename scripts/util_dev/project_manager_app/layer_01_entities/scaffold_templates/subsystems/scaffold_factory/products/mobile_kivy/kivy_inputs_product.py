from ..abstract.i_inputs_product import AbstractInputs

class KivyInputs(AbstractInputs):
    def get_template(self) -> str:
        return '''from kivy.uix.textinput import TextInput

class FormTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0.094, 0.094, 0.145, 1)  # #181825
        self.foreground_color = (0.804, 0.839, 0.957, 1)  # #cdd6f4
        self.multiline = False
        self.padding = [10, 10, 10, 10]
'''
