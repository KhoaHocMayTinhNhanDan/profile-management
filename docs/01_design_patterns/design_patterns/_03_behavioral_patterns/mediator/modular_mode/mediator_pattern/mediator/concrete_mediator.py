from .mediator_interface import (
    MediatorInterface,
)

from ..component.button import (
    Button,
)

from ..component.textbox import (
    TextBox,
)

from ..component.checkbox import (
    Checkbox,
)


class ConcreteMediator(
    MediatorInterface
):
    """
    Role: ConcreteMediator
    Description: Core participant in the Concrete Mediator.Py structure.
    """

    def __init__(self):

        # ==================================================
        # Mediator quản lý toàn bộ components
        # ==================================================

        self.checkbox = Checkbox(self)

        self.textbox = TextBox(self)

        self.button = Button(self)

    def notify(
        self,
        sender,
        event: str,
    ):

        # ==================================================
        # Checkbox event
        # ==================================================

        if (
            isinstance(sender, Checkbox)
            and event == "check"
        ):

            print(
                "[Mediator] Enable textbox."
            )

        # ==================================================
        # Textbox event
        # ==================================================

        elif (
            isinstance(sender, TextBox)
            and event == "input"
        ):

            print(
                "[Mediator] Validate input."
            )

        # ==================================================
        # Button event
        # ==================================================

        elif (
            isinstance(sender, Button)
            and event == "click"
        ):

            print(
                "[Mediator] Submit form."
            )