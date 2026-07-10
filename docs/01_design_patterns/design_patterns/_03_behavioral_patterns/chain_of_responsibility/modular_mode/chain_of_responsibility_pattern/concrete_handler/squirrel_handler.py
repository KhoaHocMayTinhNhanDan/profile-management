# =========================================================
# File:
# chain_of_responsibility/modular_mode/
# chain_of_responsibility_pattern/concrete_handler/
# squirrel_handler.py
# =========================================================

from ..handler.abstract_handler import (
    AbstractHandler,
)


class SquirrelHandler(AbstractHandler):
    """
    Role: SquirrelHandler
    Description: Core participant in the Squirrel Handler.Py structure.
    """

    def handle(
        self,
        request: str,
    ):

        if request == "Nut":

            return (
                "Squirrel: I'll eat the Nut."
            )

        return super().handle(request)