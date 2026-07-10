# =========================================================
# File:
# chain_of_responsibility/modular_mode/
# chain_of_responsibility_pattern/concrete_handler/
# monkey_handler.py
# =========================================================

from ..handler.abstract_handler import (
    AbstractHandler,
)


class MonkeyHandler(AbstractHandler):
    """
    Role: MonkeyHandler
    Description: Core participant in the Monkey Handler.Py structure.
    """

    def handle(
        self,
        request: str,
    ):

        if request == "Banana":

            return (
                "Monkey: I'll eat the Banana."
            )

        return super().handle(request)