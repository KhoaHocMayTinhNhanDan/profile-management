from ..abstract.abstract_product_a import (
    AbstractProductA,
)

from ..abstract.abstract_product_b import (
    AbstractProductB,
)

class ConcreteProductB1(AbstractProductB):
    """
    Role: ConcreteProductB1
    Description: Core participant in the Concrete Product B1.Py structure.
    """

    def useful_function_b(self) -> str:
        return "Result from ConcreteProductB1"

    def another_useful_function_b(
        self,
        collaborator: AbstractProductA,
    ) -> str:

        result = collaborator.useful_function_a()

        return (
            f"ConcreteProductB1 collaborating with -> ({result})"
        )