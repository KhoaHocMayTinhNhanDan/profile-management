# =========================================================
# File:
# bridge/modular_mode/bridge_pattern/abstraction/refined_abstraction.py
# =========================================================

from .abstraction import Abstraction


class RefinedAbstraction(Abstraction):
    """
    Role: RefinedAbstraction
    Description: Core participant in the Refined Abstraction.Py structure.
    """

    def operation(self):

        return (
            "RefinedAbstraction delegates to:\n"
            f"{self.implementation.operation_implementation()}"
        )