# =========================================================
# File:
# composite/modular_mode/composite_pattern/component/component.py
# =========================================================

from abc import ABC, abstractmethod


class Component(ABC):
    """
    Role: Component
    Description: Core participant in the Composite Pattern structure.
    """

    @abstractmethod
    def operation(self):
        pass

    def add(self, component):

        raise NotImplementedError()

    def remove(self, component):

        raise NotImplementedError()

    def is_composite(self):

        return False