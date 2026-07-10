from ..abstract.abstract_product_a import (
    AbstractProductA,
)

from ..abstract.abstract_product_b import (
    AbstractProductB,
)


class ConcreteProductB2(AbstractProductB):
    """
    Role: ConcreteProductB2
    Description: Core participant in the Concrete Product B2.Py structure.
    """

    def useful_function_b(self) -> str:
        return "Result from ConcreteProductB2"

    def another_useful_function_b(
        self,
        collaborator: AbstractProductA,
    ) -> str:

        result = collaborator.useful_function_a()

        return (
            f"ConcreteProductB2 collaborating with -> ({result})"
        )