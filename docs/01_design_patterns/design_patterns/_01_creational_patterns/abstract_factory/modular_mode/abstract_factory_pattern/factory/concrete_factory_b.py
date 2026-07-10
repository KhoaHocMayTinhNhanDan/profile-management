from .abstract_factory import (
    AbstractFactory,
)

from ..products.variant_b.concrete_product_a2 import (
    ConcreteProductA2,
)

from ..products.variant_b.concrete_product_b2 import (
    ConcreteProductB2,
)


class ConcreteFactoryB(AbstractFactory):
    """
    Role: ConcreteFactoryB
    Description: Core participant in the Concrete Factory B.Py structure.
    """

    def create_product_a(self):
        return ConcreteProductA2()

    def create_product_b(self):
        return ConcreteProductB2()