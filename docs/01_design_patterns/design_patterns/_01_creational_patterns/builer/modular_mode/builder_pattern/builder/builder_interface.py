# =========================================================
# File:
# builder/modular_mode/builder_pattern/builder/builder_interface.py
# =========================================================

from abc import ABC, abstractmethod


class BuilderInterface(ABC):
    """
    Role: BuilderInterface
    Description: Core participant in the Builder Interface.Py structure.
    """

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def build_part_a(self):
        pass

    @abstractmethod
    def build_part_b(self):
        pass

    @abstractmethod
    def build_part_c(self):
        pass