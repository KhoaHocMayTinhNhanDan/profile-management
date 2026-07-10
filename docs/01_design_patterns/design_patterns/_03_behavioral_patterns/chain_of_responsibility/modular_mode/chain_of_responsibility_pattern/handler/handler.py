# =========================================================
# File:
# chain_of_responsibility/modular_mode/
# chain_of_responsibility_pattern/handler/handler.py
# =========================================================

from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)

from typing import (
    Optional,
)


class Handler(ABC):
    """
    Role: Handler
    Description: Core participant in the Chain Of Responsibility Pattern structure.
    """

    @abstractmethod
    def set_next(
        self,
        handler: Handler,
    ) -> Handler:
        pass

    @abstractmethod
    def handle(
        self,
        request: str,
    ) -> Optional[str]:
        pass