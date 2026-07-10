# =========================================================
# File:
# bridge/modular_mode/bridge_pattern/implementation/implementation.py
# =========================================================

from abc import ABC, abstractmethod


class Implementation(ABC):
    """
    Role: Implementation
    Description: Core participant in the Bridge Pattern structure.
    """

    @abstractmethod
    def operation_implementation(self):
        pass