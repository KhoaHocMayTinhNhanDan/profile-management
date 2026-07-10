from abc import ABC, abstractmethod
from ..product.product_interface import ProductInterface


class Creator(ABC):

    @abstractmethod
    def factory_method(self) -> ProductInterface:
        pass

    def some_operation(self) -> str:
        product = self.factory_method()
        return f"Creator: working with ({product.operation()})"