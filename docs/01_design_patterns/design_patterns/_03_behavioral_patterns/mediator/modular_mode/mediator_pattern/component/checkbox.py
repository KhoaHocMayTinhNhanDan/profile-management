from .base_component import (
    BaseComponent,
)


class Checkbox(BaseComponent):
    """
    Role: Checkbox
    Description: Core participant in the Mediator Pattern structure.
    """

    def check(self):

        print(
            "[Checkbox] Checked."
        )

        self._mediator.notify(
            self,
            "check",
        )