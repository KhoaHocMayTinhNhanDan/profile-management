# =========================================================
# File:
# chain_of_responsibility/modular_mode/
# chain_of_responsibility_pattern/concrete_handler/
# dog_handler.py
# =========================================================

from ..handler.abstract_handler import (
    AbstractHandler,
)


class DogHandler(AbstractHandler):
    """
    Role: DogHandler
    Description: Core participant in the Dog Handler.Py structure.
    """

    def handle(
        self,
        request: str,
    ):

        if request == "MeatBall":

            return (
                "Dog: I'll eat the MeatBall."
            )

        return super().handle(request)