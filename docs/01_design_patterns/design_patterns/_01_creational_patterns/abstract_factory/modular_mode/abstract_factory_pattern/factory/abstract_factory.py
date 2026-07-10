# =========================================================
# File: abstract_factory/modular_mode/abstract_factory_pattern/factory/abstract_factory.py
# =========================================================

from abc import ABC, abstractmethod

from ..products.abstract.abstract_product_a import (
    AbstractProductA,
)

from ..products.abstract.abstract_product_b import (
    AbstractProductB,
)


class AbstractFactory(ABC):
    """
    Role: AbstractFactory
    Description: Core participant in the Abstract Factory.Py structure.
    """

    @abstractmethod
    def create_product_a(self) -> AbstractProductA:
        pass

    @abstractmethod
    def create_product_b(self) -> AbstractProductB:
        pass