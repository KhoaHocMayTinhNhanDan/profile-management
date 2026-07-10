from .abstract_factory import (
    AbstractFactory,
)

from ..products.variant_a.concrete_product_a1 import (
    ConcreteProductA1,
)

from ..products.variant_a.concrete_product_b1 import (
    ConcreteProductB1,
)


class ConcreteFactoryA(AbstractFactory):
    """
    Role: ConcreteFactoryA
    Description: Core participant in the Concrete Factory A.Py structure.
    """

    def create_product_a(self):
        return ConcreteProductA1()

    def create_product_b(self):
        return ConcreteProductB1()