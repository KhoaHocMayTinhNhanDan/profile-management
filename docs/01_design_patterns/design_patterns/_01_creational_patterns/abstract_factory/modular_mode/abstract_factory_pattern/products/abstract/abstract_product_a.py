# =========================================================
# File: abstract_factory/modular_mode/abstract_factory_pattern/products/abstract/abstract_product_a.py
# =========================================================

from abc import ABC, abstractmethod


class AbstractProductA(ABC):
    """
    Role: AbstractProductA
    Description: Core participant in the Abstract Product A.Py structure.
    """

    @abstractmethod
    def useful_function_a(self) -> str:
        pass