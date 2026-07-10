# =========================================================
# File:
# chain_of_responsibility/modular_mode/
# chain_of_responsibility_pattern/handler/
# abstract_handler.py
# =========================================================

from __future__ import annotations

from typing import (
    Optional,
)

from .handler import (
    Handler,
)


class AbstractHandler(Handler):
    """
    Role: AbstractHandler
    Description: Core participant in the Abstract Handler.Py structure.
    """

    def __init__(self):

        self._next_handler = None

    def set_next(
        self,
        handler: Handler,
    ) -> Handler:

        self._next_handler = handler

        return handler

    def handle(
        self,
        request: str,
    ) -> Optional[str]:

        """
        ====================================================
        Default behavior:
        forward request
        ====================================================
        """

        if self._next_handler:

            return self._next_handler.handle(
                request
            )

        return None