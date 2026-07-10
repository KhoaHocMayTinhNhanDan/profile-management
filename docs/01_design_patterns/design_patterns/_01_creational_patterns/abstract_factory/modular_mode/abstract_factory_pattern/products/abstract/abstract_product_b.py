# =========================================================
# File: abstract_factory/modular_mode/abstract_factory_pattern/products/abstract/abstract_product_b.py
# =========================================================

from abc import ABC, abstractmethod


class AbstractProductB(ABC):
    """
    Role: AbstractProductB
    Description: Core participant in the Abstract Product B.Py structure.
    """

    @abstractmethod
    def useful_function_b(self) -> str:
        pass

    @abstractmethod
    def another_useful_function_b(
        self,
        collaborator: "AbstractProductA",
    ) -> str:
        pass