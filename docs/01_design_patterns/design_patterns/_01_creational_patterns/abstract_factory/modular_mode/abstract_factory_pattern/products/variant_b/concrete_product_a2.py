from ..abstract.abstract_product_a import (
    AbstractProductA,
)


class ConcreteProductA2(AbstractProductA):
    """
    Role: ConcreteProductA2
    Description: Core participant in the Concrete Product A2.Py structure.
    """

    def useful_function_a(self) -> str:
        return "Result from ConcreteProductA2"