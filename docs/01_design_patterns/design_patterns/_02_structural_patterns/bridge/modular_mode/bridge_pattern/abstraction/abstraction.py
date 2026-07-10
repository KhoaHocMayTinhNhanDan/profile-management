# =========================================================
# File:
# bridge/modular_mode/bridge_pattern/abstraction/abstraction.py
# =========================================================

from ..implementation.implementation import (
    Implementation,
)


class Abstraction:
    """
    Role: Abstraction
    Description: Core participant in the Bridge Pattern structure.
    """

    def __init__(
        self,
        implementation: Implementation,
    ):

        self.implementation = implementation

    def operation(self):

        return (
            "Abstraction delegates to:\n"
            f"{self.implementation.operation_implementation()}"
        )