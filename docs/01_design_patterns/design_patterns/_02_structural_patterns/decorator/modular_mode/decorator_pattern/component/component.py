# =========================================================
# File:
# decorator/modular_mode/decorator_pattern/component/component.py
# =========================================================

from abc import ABC, abstractmethod


class Component(ABC):
    """
    Role: Component
    Description: Core participant in the Decorator Pattern structure.
    """

    @abstractmethod
    def operation(self):
        pass