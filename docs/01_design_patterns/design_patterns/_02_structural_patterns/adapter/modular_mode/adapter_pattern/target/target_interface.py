# =========================================================
# File:
# adapter/modular_mode/adapter_pattern/target/target_interface.py
# =========================================================

from abc import ABC, abstractmethod


class TargetInterface(ABC):
    """
    Role: TargetInterface
    Description: Core participant in the Target Interface.Py structure.
    """

    @abstractmethod
    def request(self):
        pass