from .creator_interface import Creator
from ..product.concrete_product_a import ConcreteProductA
from ..product.product_interface import ProductInterface


class ConcreteCreatorA(Creator):

    def factory_method(self) -> ProductInterface:
        return ConcreteProductA()