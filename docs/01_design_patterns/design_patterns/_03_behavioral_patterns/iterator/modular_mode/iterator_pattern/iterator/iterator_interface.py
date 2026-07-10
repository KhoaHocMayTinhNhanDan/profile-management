# =========================================================
# File:
# iterator/modular_mode/iterator_pattern/iterator/iterator_interface.py
# =========================================================

from abc import ABC, abstractmethod


class IteratorInterface(ABC):
    """
    Role: IteratorInterface
    Description: Core participant in the Iterator Interface.Py structure.
    """

    @abstractmethod
    def has_next(self):
        pass

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def current(self):
        pass

    @abstractmethod
    def reset(self):
        pass