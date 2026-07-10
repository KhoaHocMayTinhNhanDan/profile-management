from .base_component import (
    BaseComponent,
)


class TextBox(BaseComponent):
    """
    Role: TextBox
    Description: Core participant in the Mediator Pattern structure.
    """

    def input_text(
        self,
        text: str,
    ):

        print(
            f"[TextBox] Input: {text}"
        )

        self._mediator.notify(
            self,
            "input",
        )