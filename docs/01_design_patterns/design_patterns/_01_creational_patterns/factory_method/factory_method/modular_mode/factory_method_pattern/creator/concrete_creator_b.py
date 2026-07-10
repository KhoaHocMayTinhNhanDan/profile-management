from .creator_interface import Creator
from ..product.concrete_product_b import ConcreteProductB
from ..product.product_interface import ProductInterface


class ConcreteCreatorB(Creator):

    def factory_method(self) -> ProductInterface:
        return ConcreteProductB()