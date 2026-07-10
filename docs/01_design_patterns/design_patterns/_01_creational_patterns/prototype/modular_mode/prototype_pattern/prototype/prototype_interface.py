# =========================================================
# File:
# prototype/modular_mode/prototype_pattern/prototype/prototype_interface.py
# =========================================================

from abc import ABC, abstractmethod


class PrototypeInterface(ABC):
    """
    Role: PrototypeInterface
    Description: Core participant in the Prototype Interface.Py structure.
    """

    @abstractmethod
    def clone(self):
        pass