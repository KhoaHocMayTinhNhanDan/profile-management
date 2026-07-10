from .base_component import (
    BaseComponent,
)


class Button(BaseComponent):
    """
    Role: Button
    Description: Core participant in the Mediator Pattern structure.
    """

    def click(self):

        print(
            "[Button] Clicked."
        )

        self._mediator.notify(
            self,
            "click",
        )