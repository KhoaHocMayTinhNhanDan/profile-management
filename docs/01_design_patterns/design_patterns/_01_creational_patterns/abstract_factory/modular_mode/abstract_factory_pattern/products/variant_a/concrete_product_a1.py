from ..abstract.abstract_product_a import (
    AbstractProductA,
)


class ConcreteProductA1(AbstractProductA):
    """
    Role: ConcreteProductA1
    Description: Core participant in the Concrete Product A1.Py structure.
    """

    def useful_function_a(self) -> str:
        return "Result from ConcreteProductA1"